

def main():
    module = AnsibleModule(argument_spec=dict(state=dict(default='present', choices=['present', 'absent'], type='str'), size=dict(type='int'), type=dict(default='rsa', choices=['rsa', 'dsa', 'rsa1', 'ecdsa', 'ed25519'], type='str'), force=dict(default=False, type='bool'), path=dict(required=True, type='path'), comment=dict(type='str')), supports_check_mode=True, add_file_common_args=True)
    base_dir = os.path.dirname(module.params['path'])
    if (not os.path.isdir(base_dir)):
        module.fail_json(name=base_dir, msg=('The directory %s does not exist or the file is not a directory' % base_dir))
    keypair = Keypair(module)
    if (keypair.state == 'present'):
        if module.check_mode:
            result = keypair.dump()
            result['changed'] = (module.params['force'] or (not keypair.isValid(module)))
            module.exit_json(**result)
        try:
            keypair.generate(module)
        except Exception as exc:
            module.fail_json(msg=to_native(exc))
    else:
        if module.check_mode:
            keypair.changed = os.path.exists(module.params['path'])
            if keypair.changed:
                keypair.fingerprint = {
                    
                }
            result = keypair.dump()
            module.exit_json(**result)
        try:
            keypair.remove()
        except Exception as exc:
            module.fail_json(msg=to_native(exc))
    result = keypair.dump()
    module.exit_json(**result)
