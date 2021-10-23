def main():
    argument_spec = dict(master=dict(required=False, type='bool'), stratum=dict(type='str'), logging=dict(required=False, type='bool'), state=dict(choices=['absent', 'present'], default='present'))
    argument_spec.update(nxos_argument_spec)
    module = AnsibleModule(argument_spec=argument_spec, required_one_of=[['master', 'logging']], supports_check_mode=True)
    warnings = list()
    check_args(module, warnings)
    master = module.params['master']
    stratum = module.params['stratum']
    logging = module.params['logging']
    state = module.params['state']
    if stratum:
        if (master is None):
            module.fail_json(msg='The master param must be supplied when stratum is supplied')
        try:
            stratum_int = int(stratum)
            if ((stratum_int < 1) or (stratum_int > 15)):
                raise ValueError
        except ValueError:
            module.fail_json(msg='Stratum must be an integer between 1 and 15')
    existing = get_ntp_options(module)
    end_state = existing
    args = dict(master=master, stratum=stratum, logging=logging)
    changed = False
    proposed = dict(((k, v) for (k, v) in args.items() if (v is not None)))
    if (master is False):
        proposed['stratum'] = None
        stratum = None
    delta = dict(set(proposed.items()).difference(existing.items()))
    delta_stratum = delta.get('stratum')
    if delta_stratum:
        delta['master'] = True
    commands = []
    if (state == 'present'):
        if delta:
            command = config_ntp_options(delta)
            if command:
                commands.append(command)
    elif (state == 'absent'):
        if existing:
            isection = dict(set(proposed.items()).intersection(existing.items()))
            command = config_ntp_options(isection, flip=True)
            if command:
                commands.append(command)
    cmds = flatten_list(commands)
    if cmds:
        if module.check_mode:
            module.exit_json(changed=True, commands=cmds)
        else:
            changed = True
            load_config(module, cmds)
            end_state = get_ntp_options(module)
            if ('configure' in cmds):
                cmds.pop(0)
    results = {
        
    }
    results['proposed'] = proposed
    results['existing'] = existing
    results['updates'] = cmds
    results['changed'] = changed
    results['warnings'] = warnings
    results['end_state'] = end_state
    module.exit_json(**results)