def main():
    argument_spec = dict(group=dict(required=True, type='str'), interface=dict(required=True), version=dict(choices=['1', '2'], default='2', required=False), priority=dict(type='str', required=False), preempt=dict(type='str', choices=['disabled', 'enabled'], required=False), vip=dict(type='str', required=False), auth_type=dict(choices=['text', 'md5'], required=False), auth_string=dict(type='str', required=False), state=dict(choices=['absent', 'present'], required=False, default='present'), include_defaults=dict(default=True), config=dict(), save=dict(type='bool', default=False))
    argument_spec.update(nxos_argument_spec)
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)
    warnings = list()
    check_args(module, warnings)
    interface = module.params['interface'].lower()
    group = module.params['group']
    version = module.params['version']
    state = module.params['state']
    priority = module.params['priority']
    preempt = module.params['preempt']
    vip = module.params['vip']
    auth_type = module.params['auth_type']
    auth_string = module.params['auth_string']
    transport = module.params['transport']
    if ((state == 'present') and (not vip)):
        module.fail_json(msg='the "vip" param is required when state=present')
    for param in ['group', 'priority']:
        if (module.params[param] is not None):
            validate_params(param, module)
    intf_type = get_interface_type(interface)
    if ((intf_type != 'ethernet') and (transport == 'cli')):
        if (is_default(interface, module) == 'DNE'):
            module.fail_json(msg='That interface does not exist yet. Create it first.', interface=interface)
        if (intf_type == 'loopback'):
            module.fail_json(msg="Loopback interfaces don't support HSRP.", interface=interface)
    mode = get_interface_mode(interface, intf_type, module)
    if (mode == 'layer2'):
        module.fail_json(msg='That interface is a layer2 port.\nMake it a layer 3 port first.', interface=interface)
    if (auth_type or auth_string):
        if (not (auth_type and auth_string)):
            module.fail_json(msg='When using auth parameters, you need BOTH auth_type AND auth_string.')
    args = dict(group=group, version=version, priority=priority, preempt=preempt, vip=vip, auth_type=auth_type, auth_string=auth_string)
    proposed = dict(((k, v) for (k, v) in args.items() if (v is not None)))
    existing = get_hsrp_group(group, interface, module)
    if (proposed.get('auth_type', None) == 'md5'):
        if (proposed['version'] == '1'):
            module.fail_json(msg="It's recommended to use HSRP v2 when auth_type=md5")
    elif ((not proposed.get('auth_type', None)) and existing):
        if ((proposed['version'] == '1') and (existing['auth_type'] == 'md5')):
            module.fail_json(msg="Existing auth_type is md5. It's recommended to use HSRP v2 when using md5")
    changed = False
    end_state = existing
    commands = []
    if (state == 'present'):
        delta = dict(set(proposed.items()).difference(existing.items()))
        if delta:
            command = get_commands_config_hsrp(delta, interface, args)
            commands.extend(command)
    elif (state == 'absent'):
        if existing:
            command = get_commands_remove_hsrp(group, interface)
            commands.extend(command)
    if commands:
        if module.check_mode:
            module.exit_json(changed=True, commands=commands)
        else:
            load_config(module, commands)
            if (transport == 'cli'):
                body = run_commands(module, commands)
                validate_config(body, vip, module)
            changed = True
            end_state = get_hsrp_group(group, interface, module)
            if ('configure' in commands):
                commands.pop(0)
    results = {
        
    }
    results['proposed'] = proposed
    results['existing'] = existing
    results['end_state'] = end_state
    results['updates'] = commands
    results['changed'] = changed
    results['warnings'] = warnings
    module.exit_json(**results)