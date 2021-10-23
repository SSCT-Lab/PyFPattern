def main():
    ' main entry point for module execution\n    '
    argument_spec = dict(banner=dict(required=True, choices=['exec', 'motd']), text=dict(), state=dict(default='present', choices=['present', 'absent']))
    argument_spec.update(nxos_argument_spec)
    required_if = [('state', 'present', ('text',))]
    module = AnsibleModule(argument_spec=argument_spec, required_if=required_if, supports_check_mode=True)
    warnings = list()
    check_args(module, warnings)
    result = {
        'changed': False,
    }
    if warnings:
        result['warnings'] = warnings
    want = map_params_to_obj(module)
    have = map_config_to_obj(module)
    commands = map_obj_to_commands(want, have, module)
    result['commands'] = commands
    if commands:
        if (not module.check_mode):
            msgs = load_config(module, commands, True)
            if msgs:
                for item in msgs:
                    if item:
                        if isinstance(item, dict):
                            err_str = item['clierror']
                        else:
                            err_str = item
                        if (('more than 40 lines' in err_str) or ('buffer overflowed' in err_str)):
                            load_config(module, commands)
        result['changed'] = True
    module.exit_json(**result)