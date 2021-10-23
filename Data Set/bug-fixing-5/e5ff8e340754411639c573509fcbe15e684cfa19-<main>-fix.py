def main():
    argument_spec = {
        'token': {
            'required': True,
            'no_log': True,
        },
        'name': {
            'required': True,
        },
        'pubkey': {
            
        },
        'state': {
            'choices': ['present', 'absent'],
            'default': 'present',
        },
        'force': {
            'default': True,
            'type': 'bool',
        },
    }
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)
    token = module.params['token']
    name = module.params['name']
    state = module.params['state']
    force = module.params['force']
    pubkey = module.params.get('pubkey')
    if pubkey:
        pubkey_parts = pubkey.split(' ')
        if (len(pubkey_parts) < 2):
            module.fail_json(msg='"pubkey" parameter has an invalid format')
    elif (state == 'present'):
        module.fail_json(msg='"pubkey" is required when state=present')
    session = GitHubSession(module, token)
    if (state == 'present'):
        result = ensure_key_present(module, session, name, pubkey, force=force, check_mode=module.check_mode)
    elif (state == 'absent'):
        result = ensure_key_absent(session, name, check_mode=module.check_mode)
    module.exit_json(**result)