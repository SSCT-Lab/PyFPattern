

def main():
    argument_spec = dict(vlan_id=dict(required=False, type='str'), vlan_range=dict(required=False), name=dict(required=False), vlan_state=dict(choices=['active', 'suspend'], required=False), mapped_vni=dict(required=False, type='str'), state=dict(choices=['present', 'absent'], default='present', required=False), admin_state=dict(choices=['up', 'down'], required=False), mode=dict(choices=['ce', 'fabricpath'], required=False))
    argument_spec.update(nxos_argument_spec)
    module = AnsibleModule(argument_spec=argument_spec, mutually_exclusive=[['vlan_range', 'name'], ['vlan_id', 'vlan_range']], supports_check_mode=True)
    warnings = list()
    check_args(module, warnings)
    results = dict(changed=False)
    vlan_range = module.params['vlan_range']
    vlan_id = module.params['vlan_id']
    name = module.params['name']
    vlan_state = module.params['vlan_state']
    admin_state = module.params['admin_state']
    mapped_vni = module.params['mapped_vni']
    state = module.params['state']
    mode = module.params['mode']
    if vlan_id:
        if (not vlan_id.isdigit()):
            module.fail_json(msg='vlan_id must be a valid VLAN ID')
    args = dict(name=name, vlan_state=vlan_state, admin_state=admin_state, mapped_vni=mapped_vni, mode=mode)
    proposed = dict(((k, v) for (k, v) in args.items() if (v is not None)))
    proposed_vlans_list = vlan_range_to_list((vlan_id or vlan_range))
    existing_vlans_list = get_list_of_vlans(module)
    commands = []
    existing = {
        
    }
    if vlan_range:
        if (state == 'present'):
            vlans_delta = numerical_sort(set(proposed_vlans_list).difference(existing_vlans_list))
            commands = build_commands(vlans_delta, state)
        elif (state == 'absent'):
            vlans_common = numerical_sort(set(proposed_vlans_list).intersection(existing_vlans_list))
            commands = build_commands(vlans_common, state)
    else:
        existing = get_vlan(vlan_id, module)
        if ((state == 'absent') and existing):
            commands = [('no vlan ' + vlan_id)]
        elif (state == 'present'):
            if ((existing.get('mapped_vni') == '0') and (proposed.get('mapped_vni') == 'default')):
                proposed.pop('mapped_vni')
            delta = dict(set(proposed.items()).difference(existing.items()))
            if (delta or (not existing)):
                commands = get_vlan_config_commands(delta, vlan_id)
    if commands:
        if existing.get('mapped_vni'):
            if ((existing.get('mapped_vni') != proposed.get('mapped_vni')) and (existing.get('mapped_vni') != '0') and (proposed.get('mapped_vni') != 'default')):
                if (state == 'absent'):
                    commands = [('vlan ' + vlan_id), 'no vn-segment', ('no vlan ' + vlan_id)]
                else:
                    commands.insert(1, 'no vn-segment')
        if module.check_mode:
            module.exit_json(changed=True, commands=commands)
        else:
            load_config(module, commands)
            results['changed'] = True
    results['commands'] = commands
    module.exit_json(**results)
