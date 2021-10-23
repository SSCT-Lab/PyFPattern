def main():
    'main entry point for module execution\n    '
    argument_spec = dict(netconf_port=dict(type='int', default=830, aliases=['listens_on']), state=dict(default='present', choices=['present', 'absent']))
    argument_spec.update(junos_argument_spec)
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)
    warnings = list()
    check_args(module, warnings)
    result = {
        'changed': False,
        'warnings': warnings,
    }
    want = map_params_to_obj(module)
    have = map_config_to_obj(module)
    commands = map_obj_to_commands((want, have), module)
    result['commands'] = commands
    if commands:
        commit = (not module.check_mode)
        diff = load_config(module, commands)
        if diff:
            if commit:
                commit_configuration(module)
            else:
                discard_changes(module)
            result['changed'] = True
            if module._diff:
                result['diff'] = {
                    'prepared': diff,
                }
    module.exit_json(**result)