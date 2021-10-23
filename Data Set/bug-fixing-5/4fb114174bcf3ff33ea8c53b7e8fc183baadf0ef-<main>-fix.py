def main():
    argument_spec = dict(flush_routes=dict(type='bool'), enforce_rtr_alert=dict(type='bool'), restart=dict(type='bool', default=False), state=dict(choices=['present', 'default'], default='present'), include_defaults=dict(default=False), config=dict(), save=dict(type='bool', default=False))
    argument_spec.update(nxos_argument_spec)
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)
    warnings = list()
    check_args(module, warnings)
    current = get_current(module)
    desired = get_desired(module)
    state = module.params['state']
    restart = module.params['restart']
    commands = list()
    if (state == 'default'):
        if current['flush_routes']:
            commands.append('no ip igmp flush-routes')
        if current['enforce_rtr_alert']:
            commands.append('no ip igmp enforce-router-alert')
    elif (state == 'present'):
        if (desired['flush_routes'] and (not current['flush_routes'])):
            commands.append('ip igmp flush-routes')
        if (desired['enforce_rtr_alert'] and (not current['enforce_rtr_alert'])):
            commands.append('ip igmp enforce-router-alert')
    result = {
        'changed': False,
        'updates': commands,
        'warnings': warnings,
    }
    if commands:
        if (not module.check_mode):
            load_config(module, commands)
        result['changed'] = True
    if module.params['restart']:
        run_commands(module, 'restart igmp')
    module.exit_json(**result)