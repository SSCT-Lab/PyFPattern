def main():
    ' main entry point for module execution\n    '
    argument_spec = dict(dest=dict(choices=DEST_GROUP), name=dict(), facility=dict(), remote_server=dict(), dest_level=dict(type='int', aliases=['level']), facility_level=dict(type='int'), state=dict(default='present', choices=['present', 'absent']), aggregate=dict(type='list'))
    argument_spec.update(nxos_argument_spec)
    required_if = [('dest', 'logfile', ['name']), ('dest', 'server', ['remote_server'])]
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
    commands = map_obj_to_commands((want, have))
    result['commands'] = commands
    if commands:
        if (not module.check_mode):
            load_config(module, commands)
        result['changed'] = True
    module.exit_json(**result)