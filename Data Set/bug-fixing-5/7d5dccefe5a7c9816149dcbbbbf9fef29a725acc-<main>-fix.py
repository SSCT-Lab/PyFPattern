def main():
    ' main entry point for module execution\n    '
    element_spec = dict(dest=dict(type='str', choices=['on', 'host', 'console', 'monitor', 'buffered']), name=dict(type='str'), size=dict(type='int'), facility=dict(type='str'), level=dict(type='str', default='debugging'), state=dict(default='present', choices=['present', 'absent']))
    aggregate_spec = deepcopy(element_spec)
    remove_default_spec(aggregate_spec)
    argument_spec = dict(aggregate=dict(type='list', elements='dict', options=aggregate_spec))
    argument_spec.update(element_spec)
    argument_spec.update(ios_argument_spec)
    required_if = [('dest', 'host', ['name'])]
    module = AnsibleModule(argument_spec=argument_spec, required_if=required_if, supports_check_mode=True)
    warnings = list()
    check_args(module, warnings)
    result = {
        'changed': False,
    }
    if warnings:
        result['warnings'] = warnings
    want = map_params_to_obj(module, required_if=required_if)
    have = map_config_to_obj(module)
    commands = map_obj_to_commands((want, have), module)
    result['commands'] = commands
    if commands:
        if (not module.check_mode):
            load_config(module, commands)
        result['changed'] = True
    module.exit_json(**result)