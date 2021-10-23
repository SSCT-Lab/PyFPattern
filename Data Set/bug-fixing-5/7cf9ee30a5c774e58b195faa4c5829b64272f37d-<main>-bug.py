def main():
    argument_spec = dict(vlan_id=dict(required=False, type='str'), vlan_range=dict(required=False), name=dict(required=False), vlan_state=dict(choices=['active', 'suspend'], required=False), mapped_vni=dict(required=False, type='str'), state=dict(choices=['present', 'absent'], default='present', required=False), admin_state=dict(choices=['up', 'down'], required=False), include_defaults=dict(default=False), config=dict(), save=dict(type='bool', default=False))
    module = get_network_module(argument_spec=argument_spec, mutually_exclusive=[['vlan_range', 'name'], ['vlan_id', 'vlan_range']], supports_check_mode=True)
    vlan_range = module.params['vlan_range']
    vlan_id = module.params['vlan_id']
    name = module.params['name']
    vlan_state = module.params['vlan_state']
    admin_state = module.params['admin_state']
    mapped_vni = module.params['mapped_vni']
    state = module.params['state']
    changed = False
    if vlan_id:
        if (not vlan_id.isdigit()):
            module.fail_json(msg='vlan_id must be a valid VLAN ID')
    args = dict(name=name, vlan_state=vlan_state, admin_state=admin_state, mapped_vni=mapped_vni)
    proposed = dict(((k, v) for (k, v) in args.items() if (v is not None)))
    proposed_vlans_list = numerical_sort(vlan_range_to_list((vlan_id or vlan_range)))
    existing_vlans_list = numerical_sort(get_list_of_vlans(module))
    commands = []
    existing = {
        
    }
    if vlan_range:
        if (state == 'present'):
            vlans_delta = list(set(proposed_vlans_list).difference(existing_vlans_list))
            commands = build_commands(vlans_delta, state)
        elif (state == 'absent'):
            vlans_common = list(set(proposed_vlans_list).intersection(existing_vlans_list))
            commands = build_commands(vlans_common, state)
    else:
        existing = get_vlan(vlan_id, module)
        if (state == 'absent'):
            if existing:
                commands = [('no vlan ' + vlan_id)]
        elif (state == 'present'):
            if ((existing.get('mapped_vni') == '0') and (proposed.get('mapped_vni') == 'default')):
                proposed.pop('mapped_vni')
            delta = dict(set(proposed.items()).difference(existing.items()))
            if (delta or (not existing)):
                commands = get_vlan_config_commands(delta, vlan_id)
    end_state = existing
    end_state_vlans_list = existing_vlans_list
    if commands:
        if existing.get('mapped_vni'):
            if ((existing.get('mapped_vni') != proposed.get('mapped_vni')) and (existing.get('mapped_vni') != '0') and (proposed.get('mapped_vni') != 'default')):
                commands.insert(1, 'no vn-segment')
        if module.check_mode:
            module.exit_json(changed=True, commands=commands)
        else:
            execute_config_command(commands, module)
            changed = True
            end_state_vlans_list = numerical_sort(get_list_of_vlans(module))
            if ('configure' in commands):
                commands.pop(0)
            if vlan_id:
                end_state = get_vlan(vlan_id, module)
    results = {
        
    }
    results['proposed_vlans_list'] = proposed_vlans_list
    results['existing_vlans_list'] = existing_vlans_list
    results['proposed'] = proposed
    results['existing'] = existing
    results['end_state'] = end_state
    results['end_state_vlans_list'] = end_state_vlans_list
    results['updates'] = commands
    results['changed'] = changed
    module.exit_json(**results)