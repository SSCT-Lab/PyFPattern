def main():
    argument_spec = dict(snooping=dict(required=False, type='bool'), group_timeout=dict(required=False, type='str'), link_local_grp_supp=dict(required=False, type='bool'), report_supp=dict(required=False, type='bool'), v3_report_supp=dict(required=False, type='bool'), state=dict(choices=['present', 'default'], default='present'))
    argument_spec.update(nxos_argument_spec)
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)
    warnings = list()
    check_args(module, warnings)
    results = {
        'changed': False,
        'commands': [],
        'warnings': warnings,
    }
    snooping = module.params['snooping']
    link_local_grp_supp = module.params['link_local_grp_supp']
    report_supp = module.params['report_supp']
    v3_report_supp = module.params['v3_report_supp']
    group_timeout = module.params['group_timeout']
    state = module.params['state']
    args = dict(snooping=snooping, link_local_grp_supp=link_local_grp_supp, report_supp=report_supp, v3_report_supp=v3_report_supp, group_timeout=group_timeout)
    proposed = dict(((param, value) for (param, value) in args.items() if (value is not None)))
    existing = get_igmp_snooping(module)
    end_state = existing
    commands = []
    if (state == 'present'):
        delta = dict(set(proposed.items()).difference(existing.items()))
        if delta:
            command = config_igmp_snooping(delta, existing)
            if command:
                commands.append(command)
    elif (state == 'default'):
        proposed = get_igmp_snooping_defaults()
        delta = dict(set(proposed.items()).difference(existing.items()))
        if delta:
            command = config_igmp_snooping(delta, existing, default=True)
            if command:
                commands.append(command)
    cmds = flatten_list(commands)
    if cmds:
        results['changed'] = True
        if (not module.check_mode):
            load_config(module, cmds)
        if ('configure' in cmds):
            cmds.pop(0)
        results['commands'] = cmds
    module.exit_json(**results)