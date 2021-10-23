def main():
    argument_spec = dict(master=dict(required=False, type='bool'), stratum=dict(type='str'), logging=dict(required=False, type='bool'), state=dict(choices=['absent', 'present'], default='present'))
    argument_spec.update(nxos_argument_spec)
    required_together = [('master', 'stratum')]
    module = AnsibleModule(argument_spec=argument_spec, required_together=required_together, supports_check_mode=True)
    warnings = list()
    check_args(module, warnings)
    master = module.params['master']
    stratum = module.params['stratum']
    logging = module.params['logging']
    state = module.params['state']
    if stratum:
        try:
            stratum_int = int(stratum)
            if ((stratum_int < 1) or (stratum_int > 15)):
                raise ValueError
        except ValueError:
            module.fail_json(msg='stratum must be an integer between 1 and 15')
    desired = {
        'master': master,
        'stratum': stratum,
        'logging': logging,
    }
    current = get_current(module)
    result = {
        'changed': False,
    }
    commands = list()
    if (state == 'absent'):
        if current['master']:
            commands.append('no ntp master')
        if current['logging']:
            commands.append('no ntp logging')
    elif (state == 'present'):
        if (desired['master'] and (desired['master'] != current['master'])):
            if desired['stratum']:
                commands.append(('ntp master %s' % stratum))
            else:
                commands.append('ntp master')
        elif (desired['stratum'] and (desired['stratum'] != current['stratum'])):
            commands.append(('ntp master %s' % stratum))
        if (desired['logging'] and (desired['logging'] != current['logging'])):
            if desired['logging']:
                commands.append('ntp logging')
            else:
                commands.append('no ntp logging')
    result['commands'] = commands
    result['updates'] = commands
    if commands:
        if (not module.check_mode):
            load_config(module, commands)
        result['changed'] = True
    result['warnings'] = warnings
    module.exit_json(**result)