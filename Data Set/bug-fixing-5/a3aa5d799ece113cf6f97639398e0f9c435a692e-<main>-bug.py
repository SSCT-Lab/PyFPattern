def main():
    ' main entry point for module execution\n    '
    argument_spec = dict(hostname=dict(), domain_lookup=dict(type='bool'), domain_name=dict(type='list'), domain_search=dict(type='list'), name_servers=dict(type='list'), system_mtu=dict(type='int'), state=dict(default='present', choices=['present', 'absent']))
    argument_spec.update(nxos_argument_spec)
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
    commands = map_obj_to_commands(want, have, module)
    result['commands'] = commands
    if commands:
        if (not module.check_mode):
            load_config(module, commands)
        result['changed'] = True
    module.exit_json(**result)