def main():
    argument_spec = dict(interface=dict(required=True, type='str'), vni=dict(required=True, type='str'), assoc_vrf=dict(required=False, type='bool'), multicast_group=dict(required=False, type='str'), peer_list=dict(required=False, type='list'), suppress_arp=dict(required=False, type='bool'), ingress_replication=dict(required=False, type='str', choices=['bgp', 'static', 'default']), state=dict(choices=['present', 'absent'], default='present', required=False))
    argument_spec.update(nxos_argument_spec)
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)
    warnings = list()
    check_args(module, warnings)
    result = {
        'changed': False,
        'commands': [],
        'warnings': warnings,
    }
    if module.params['assoc_vrf']:
        mutually_exclusive_params = ['multicast_group', 'suppress_arp', 'ingress_replication']
        for param in mutually_exclusive_params:
            if module.params[param]:
                module.fail_json(msg='assoc_vrf cannot be used with {0} param'.format(param))
    if module.params['peer_list']:
        if (module.params['ingress_replication'] != 'static'):
            module.fail_json(msg='ingress_replication=static is required when using peer_list param')
        else:
            peer_list = module.params['peer_list']
            if (peer_list[0] == 'default'):
                module.params['peer_list'] = 'default'
            else:
                stripped_peer_list = map(str.strip, peer_list)
                module.params['peer_list'] = stripped_peer_list
    state = module.params['state']
    args = PARAM_TO_COMMAND_KEYMAP.keys()
    (existing, interface_exist) = get_existing(module, args)
    if (state == 'present'):
        if (not interface_exist):
            module.fail_json(msg='The proposed NVE interface does not exist. Use nxos_interface to create it first.')
        elif (interface_exist != module.params['interface']):
            module.fail_json(msg='Only 1 NVE interface is allowed on the switch.')
    elif (state == 'absent'):
        if (interface_exist != module.params['interface']):
            module.exit_json(**result)
        elif (existing and (existing['vni'] != module.params['vni'])):
            module.fail_json(msg='ERROR: VNI delete failed: Could not find vni node for {0}'.format(module.params['vni']), existing_vni=existing['vni'])
    proposed_args = dict(((k, v) for (k, v) in module.params.items() if ((v is not None) and (k in args))))
    proposed = {
        
    }
    for (key, value) in proposed_args.items():
        if ((key != 'interface') and (existing.get(key) != value)):
            proposed[key] = value
    candidate = CustomNetworkConfig(indent=3)
    if (state == 'present'):
        state_present(module, existing, proposed, candidate)
    elif (state == 'absent'):
        state_absent(module, existing, proposed, candidate)
    if candidate:
        candidate = candidate.items_text()
        result['changed'] = True
        result['commands'] = candidate
        if (not module.check_mode):
            load_config(module, candidate)
    module.exit_json(**result)