def main():
    ' main entry point for module execution\n    '
    argument_spec = dict(name=dict(required=True), interfaces=dict(type='list'), rd=dict(), aggregate=dict(), purge=dict(default=False, type='bool'), state=dict(default='present', choices=['present', 'absent']))
    argument_spec.update(eos_argument_spec)
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)
    warnings = list()
    check_args(module, warnings)
    result = {
        'changed': False,
    }
    if warnings:
        result['warnings'] = warnings
    want = map_params_to_obj(module)
    have = map_config_to_obj(module)
    commands = map_obj_to_commands((want, have), module)
    result['commands'] = commands
    if commands:
        commit = (not module.check_mode)
        response = load_config(module, commands, commit=commit)
        if (response.get('diff') and module._diff):
            result['diff'] = {
                'prepared': response.get('diff'),
            }
        result['session_name'] = response.get('session')
        result['changed'] = True
    module.exit_json(**result)