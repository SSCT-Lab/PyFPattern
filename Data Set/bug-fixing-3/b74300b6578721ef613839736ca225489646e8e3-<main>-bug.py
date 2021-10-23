def main():
    argument_spec = dict(interface=dict(required=True, type='str'), ospf=dict(required=True, type='str'), area=dict(required=True, type='str'), cost=dict(required=False, type='str'), hello_interval=dict(required=False, type='str'), dead_interval=dict(required=False, type='str'), passive_interface=dict(required=False, type='bool'), message_digest=dict(required=False, type='bool'), message_digest_key_id=dict(required=False, type='str'), message_digest_algorithm_type=dict(required=False, type='str', choices=['md5']), message_digest_encryption_type=dict(required=False, type='str', choices=['cisco_type_7', '3des']), message_digest_password=dict(required=False, type='str', no_log=True), state=dict(choices=['present', 'absent'], default='present', required=False), include_defaults=dict(default=True), config=dict(), save=dict(type='bool', default=False))
    argument_spec.update(nxos_argument_spec)
    module = AnsibleModule(argument_spec=argument_spec, required_together=[['message_digest_key_id', 'message_digest_algorithm_type', 'message_digest_encryption_type', 'message_digest_password']], supports_check_mode=True)
    if (not module.params['interface'].startswith('loopback')):
        module.params['interface'] = module.params['interface'].capitalize()
    warnings = list()
    check_args(module, warnings)
    result = {
        'changed': False,
        'commands': [],
        'warnings': warnings,
    }
    for param in ['message_digest_encryption_type', 'message_digest_algorithm_type', 'message_digest_password']:
        if (module.params[param] == 'default'):
            module.exit_json(msg='Use message_digest_key_id=default to remove an existing authentication configuration')
    state = module.params['state']
    args = PARAM_TO_COMMAND_KEYMAP.keys()
    existing = get_existing(module, args)
    proposed_args = dict(((k, v) for (k, v) in module.params.items() if ((v is not None) and (k in args))))
    proposed = {
        
    }
    for (key, value) in proposed_args.items():
        if (key != 'interface'):
            if (str(value).lower() == 'true'):
                value = True
            elif (str(value).lower() == 'false'):
                value = False
            elif (str(value).lower() == 'default'):
                value = 'default'
            if (existing.get(key) or ((not existing.get(key)) and value)):
                proposed[key] = value
    proposed['area'] = normalize_area(proposed['area'], module)
    candidate = CustomNetworkConfig(indent=3)
    if (state == 'present'):
        state_present(module, existing, proposed, candidate)
    elif ((state == 'absent') and (existing.get('ospf') == proposed['ospf']) and (existing.get('area') == proposed['area'])):
        state_absent(module, existing, proposed, candidate)
    if candidate:
        candidate = candidate.items_text()
        load_config(module, candidate)
        result['changed'] = True
        result['commands'] = candidate
    module.exit_json(**result)