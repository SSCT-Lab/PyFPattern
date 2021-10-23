def main():
    argument_spec = dict(interface=dict(required=True, type='str'), version=dict(required=False, type='str'), startup_query_interval=dict(required=False, type='str'), startup_query_count=dict(required=False, type='str'), robustness=dict(required=False, type='str'), querier_timeout=dict(required=False, type='str'), query_mrt=dict(required=False, type='str'), query_interval=dict(required=False, type='str'), last_member_qrt=dict(required=False, type='str'), last_member_query_count=dict(required=False, type='str'), group_timeout=dict(required=False, type='str'), report_llg=dict(type='bool'), immediate_leave=dict(type='bool'), oif_routemap=dict(required=False, type='str'), oif_prefix=dict(required=False, type='str', removed_in_version='2.10'), oif_source=dict(required=False, type='str', removed_in_version='2.10'), oif_ps=dict(required=False, type='raw'), restart=dict(type='bool', default=False), state=dict(choices=['present', 'absent', 'default'], default='present'))
    argument_spec.update(nxos_argument_spec)
    mutually_exclusive = [('oif_ps', 'oif_prefix'), ('oif_ps', 'oif_source'), ('oif_ps', 'oif_routemap'), ('oif_prefix', 'oif_routemap')]
    module = AnsibleModule(argument_spec=argument_spec, mutually_exclusive=mutually_exclusive, supports_check_mode=True)
    warnings = list()
    check_args(module, warnings)
    state = module.params['state']
    interface = module.params['interface']
    oif_prefix = module.params['oif_prefix']
    oif_source = module.params['oif_source']
    oif_routemap = module.params['oif_routemap']
    oif_ps = module.params['oif_ps']
    if (oif_source and (not oif_prefix)):
        module.fail_json(msg='oif_prefix required when setting oif_source')
    elif (oif_source and oif_prefix):
        oif_ps = [{
            'source': oif_source,
            'prefix': oif_prefix,
        }]
    elif ((not oif_source) and oif_prefix):
        oif_ps = [{
            'prefix': oif_prefix,
        }]
    intf_type = get_interface_type(interface)
    if (get_interface_mode(interface, intf_type, module) == 'layer2'):
        module.fail_json(msg='this module only works on Layer 3 interfaces')
    existing = get_igmp_interface(module, interface)
    existing_copy = existing.copy()
    end_state = existing_copy
    if (not existing.get('version')):
        module.fail_json(msg='pim needs to be enabled on the interface')
    existing_oif_prefix_source = existing.get('oif_prefix_source')
    existing.pop('oif_prefix_source')
    if (oif_routemap and existing_oif_prefix_source):
        module.fail_json(msg='Delete static-oif configurations on this interface if you want to use a routemap')
    if (oif_ps and existing.get('oif_routemap')):
        module.fail_json(msg='Delete static-oif route-map configuration on this interface if you want to config static entries')
    args = ['version', 'startup_query_interval', 'startup_query_count', 'robustness', 'querier_timeout', 'query_mrt', 'query_interval', 'last_member_qrt', 'last_member_query_count', 'group_timeout', 'report_llg', 'immediate_leave', 'oif_routemap']
    changed = False
    commands = []
    proposed = dict(((k, v) for (k, v) in module.params.items() if ((v is not None) and (k in args))))
    CANNOT_ABSENT = ['version', 'startup_query_interval', 'startup_query_count', 'robustness', 'querier_timeout', 'query_mrt', 'query_interval', 'last_member_qrt', 'last_member_query_count', 'group_timeout', 'report_llg', 'immediate_leave']
    if (state == 'absent'):
        for each in CANNOT_ABSENT:
            if (each in proposed):
                module.fail_json(msg='only params: oif_prefix, oif_source, oif_ps, oif_routemap can be used when state=absent')
    delta = dict(set(proposed.items()).difference(existing.items()))
    if oif_ps:
        if (oif_ps == 'default'):
            delta['oif_ps'] = []
        else:
            delta['oif_ps'] = oif_ps
    if (state == 'present'):
        if delta:
            command = config_igmp_interface(delta, existing, existing_oif_prefix_source)
            if command:
                commands.append(command)
    elif (state == 'default'):
        command = config_default_igmp_interface(existing, delta)
        if command:
            commands.append(command)
    elif (state == 'absent'):
        command = None
        if (existing.get('oif_routemap') or existing_oif_prefix_source):
            command = config_remove_oif(existing, existing_oif_prefix_source)
        if command:
            commands.append(command)
        command = config_default_igmp_interface(existing, delta)
        if command:
            commands.append(command)
    cmds = []
    results = {
        
    }
    if commands:
        commands.insert(0, ['interface {0}'.format(interface)])
        cmds = flatten_list(commands)
        if module.check_mode:
            module.exit_json(changed=True, commands=cmds)
        else:
            load_config(module, cmds)
            changed = True
            end_state = get_igmp_interface(module, interface)
            if ('configure' in cmds):
                cmds.pop(0)
    if module.params['restart']:
        cmd = {
            'command': 'restart igmp',
            'output': 'text',
        }
        run_commands(module, cmd)
    results['proposed'] = proposed
    results['existing'] = existing_copy
    results['updates'] = cmds
    results['changed'] = changed
    results['warnings'] = warnings
    results['end_state'] = end_state
    module.exit_json(**results)