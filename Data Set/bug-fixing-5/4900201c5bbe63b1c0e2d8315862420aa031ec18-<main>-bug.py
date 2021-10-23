def main():
    argument_spec = ec2_argument_spec()
    argument_spec.update(dict(instance_id=dict(required=True), key_file=dict(required=True), key_passphrase=dict(no_log=True, default=None, required=False), wait=dict(type='bool', default=False, required=False), wait_timeout=dict(default=120, required=False)))
    module = AnsibleModule(argument_spec=argument_spec)
    if (not HAS_BOTO):
        module.fail_json(msg='Boto required for this module.')
    instance_id = module.params.get('instance_id')
    key_file = expanduser(module.params.get('key_file'))
    key_passphrase = module.params.get('key_passphrase')
    wait = module.params.get('wait')
    wait_timeout = int(module.params.get('wait_timeout'))
    ec2 = ec2_connect(module)
    if wait:
        start = datetime.datetime.now()
        end = (start + datetime.timedelta(seconds=wait_timeout))
        while (datetime.datetime.now() < end):
            data = ec2.get_password_data(instance_id)
            decoded = b64decode(data)
            if (wait and (not decoded)):
                time.sleep(5)
            else:
                break
    else:
        data = ec2.get_password_data(instance_id)
        decoded = b64decode(data)
    if (wait and (datetime.datetime.now() >= end)):
        module.fail_json(msg=('wait for password timeout after %d seconds' % wait_timeout))
    try:
        f = open(key_file, 'r')
    except IOError as e:
        module.fail_json(msg=('I/O error (%d) opening key file: %s' % (e.errno, e.strerror)))
    else:
        try:
            with f:
                key = RSA.importKey(f.read(), key_passphrase)
        except (ValueError, IndexError, TypeError) as e:
            module.fail_json(msg='unable to parse key file')
    cipher = PKCS1_v1_5.new(key)
    sentinel = 'password decryption failed!!!'
    try:
        decrypted = cipher.decrypt(decoded, sentinel)
    except ValueError as e:
        decrypted = None
    if (decrypted is None):
        module.exit_json(win_password='', changed=False)
    elif wait:
        elapsed = (datetime.datetime.now() - start)
        module.exit_json(win_password=decrypted, changed=True, elapsed=elapsed.seconds)
    else:
        module.exit_json(win_password=decrypted, changed=True)