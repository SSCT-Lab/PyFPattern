def main():
    argument_spec = dict(vrf=dict(required=True), description=dict(default=None, required=False), vni=dict(required=False, type='str'), rd=dict(required=False, type='str'), admin_state=dict(default='up', choices=['up', 'down'], required=False), state=dict(default='present', choices=['present', 'absent'], required=False), include_defaults=dict(default=False), config=dict(), save=dict(type='bool', default=False))
    argument_spec.update(nxos_argument_spec)
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)
    warnings = list()
    check_args(module, warnings)
    results = dict(changed=False, warnings=warnings)
    vrf = module.params['vrf']
    admin_state = module.params['admin_state'].lower()
    description = module.params['description']
    rd = module.params['rd']
    vni = module.params['vni']
    state = module.params['state']
    if (vrf == 'default'):
        module.fail_json(msg='cannot use default as name of a VRF')
    elif (len(vrf) > 32):
        module.fail_json(msg='VRF name exceeded max length of 32', vrf=vrf)
    existing = get_vrf(vrf, module)
    args = dict(vrf=vrf, description=description, vni=vni, admin_state=admin_state, rd=rd)
    proposed = dict(((k, v) for (k, v) in args.items() if (v is not None)))
    delta = dict(set(proposed.items()).difference(existing.items()))
    commands = []
    if (state == 'absent'):
        if existing:
            command = ['no vrf context {0}'.format(vrf)]
            commands.extend(command)
    elif (state == 'present'):
        if (not existing):
            command = get_commands_to_config_vrf(delta, vrf)
            commands.extend(command)
        elif delta:
            command = get_commands_to_config_vrf(delta, vrf)
            commands.extend(command)
    if ((state == 'present') and commands):
        if proposed.get('vni'):
            if (existing.get('vni') and (existing.get('vni') != '')):
                commands.insert(1, 'no vni {0}'.format(existing['vni']))
    if (commands and (not module.check_mode)):
        load_config(module, commands)
        results['changed'] = True
        if ('configure' in commands):
            commands.pop(0)
    results['commands'] = commands
    module.exit_json(**results)