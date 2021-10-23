def main():
    argument_spec = dict(commands=dict(required=False, type='list'), mode=dict(required=True, choices=['maintenance', 'normal']), state=dict(choices=['absent', 'present'], default='present'), include_defaults=dict(default=False), config=dict())
    argument_spec.update(nxos_argument_spec)
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)
    warnings = list()
    check_args(module, warnings)
    state = module.params['state']
    commands = (module.params['commands'] or [])
    if ((state == 'absent') and commands):
        module.fail_json(msg='when state is absent, no command can be used.')
    existing = invoke('get_existing', module)
    end_state = existing
    changed = False
    result = {
        
    }
    cmds = []
    if ((state == 'present') or ((state == 'absent') and existing)):
        cmds = invoke(('state_%s' % state), module, existing, commands)
        if module.check_mode:
            module.exit_json(changed=True, commands=cmds)
        else:
            load_config(module, cmds)
            changed = True
            end_state = invoke('get_existing', module)
    result['changed'] = changed
    if (module._verbosity > 0):
        end_state = invoke('get_existing', module)
        result['end_state'] = end_state
        result['existing'] = existing
        result['proposed'] = commands
        result['updates'] = cmds
    result['warnings'] = warnings
    module.exit_json(**result)