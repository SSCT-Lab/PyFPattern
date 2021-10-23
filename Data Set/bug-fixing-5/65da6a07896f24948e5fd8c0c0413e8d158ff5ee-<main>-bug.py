def main():
    argument_spec = ec2_argument_spec()
    argument_spec.update(dict(name=dict(required=True), key_material=dict(required=False), force=dict(required=False, type='bool', default=True), state=dict(default='present', choices=['present', 'absent']), wait=dict(type='bool', default=False), wait_timeout=dict(default=300)))
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)
    if (not HAS_BOTO):
        module.fail_json(msg='boto required for this module')
    name = module.params['name']
    state = module.params.get('state')
    key_material = module.params.get('key_material')
    force = module.params.get('force')
    wait = module.params.get('wait')
    wait_timeout = int(module.params.get('wait_timeout'))
    changed = False
    ec2 = ec2_connect(module)
    key = ec2.get_key_pair(name)
    if (state == 'absent'):
        if key:
            'found a match, delete it'
            if (not module.check_mode):
                try:
                    key.delete()
                    if wait:
                        start = time.time()
                        action_complete = False
                        while ((time.time() - start) < wait_timeout):
                            if (not ec2.get_key_pair(name)):
                                action_complete = True
                                break
                            time.sleep(1)
                        if (not action_complete):
                            module.fail_json(msg='timed out while waiting for the key to be removed')
                except Exception as e:
                    module.fail_json(msg=("Unable to delete key pair '%s' - %s" % (key, e)))
            key = None
            changed = True
    elif (state == 'present'):
        if key:
            if (key_material and force):
                test = 'empty'
                while test:
                    randomchars = [random.choice((string.ascii_letters + string.digits)) for x in range(0, 10)]
                    tmpkeyname = ('ansible-' + ''.join(randomchars))
                    test = ec2.get_key_pair(tmpkeyname)
                tmpkey = ec2.import_key_pair(tmpkeyname, key_material)
                tmpfingerprint = tmpkey.fingerprint
                tmpkey.delete()
                if (key.fingerprint != tmpfingerprint):
                    if (not module.check_mode):
                        key.delete()
                        key = ec2.import_key_pair(name, key_material)
                        if wait:
                            start = time.time()
                            action_complete = False
                            while ((time.time() - start) < wait_timeout):
                                if ec2.get_key_pair(name):
                                    action_complete = True
                                    break
                                time.sleep(1)
                            if (not action_complete):
                                module.fail_json(msg='timed out while waiting for the key to be re-created')
                    changed = True
            pass
        else:
            'no match found, create it'
            if (not module.check_mode):
                if key_material:
                    'We are providing the key, need to import'
                    key = ec2.import_key_pair(name, to_bytes(key_material))
                else:
                    '\n                    No material provided, let AWS handle the key creation and\n                    retrieve the private key\n                    '
                    key = ec2.create_key_pair(name)
                if wait:
                    start = time.time()
                    action_complete = False
                    while ((time.time() - start) < wait_timeout):
                        if ec2.get_key_pair(name):
                            action_complete = True
                            break
                        time.sleep(1)
                    if (not action_complete):
                        module.fail_json(msg='timed out while waiting for the key to be created')
            changed = True
    if key:
        data = {
            'name': key.name,
            'fingerprint': key.fingerprint,
        }
        if key.material:
            data.update({
                'private_key': key.material,
            })
        module.exit_json(changed=changed, key=data)
    else:
        module.exit_json(changed=changed, key=None)