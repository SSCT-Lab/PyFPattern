

def main():
    argument_spec = dict(host_name=dict(type='str'), domain_name=dict(type='str'), domain_search=dict(type='list'), name_server=dict(type='list'), state=dict(type='str', default='present', choices=['present', 'absent']))
    argument_spec.update(vyos_argument_spec)
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True, mutually_exclusive=[('domain_name', 'domain_search')])
    warnings = list()
    check_args(module, warnings)
    result = {
        'changed': False,
        'warnings': warnings,
    }
    want = map_param_to_obj(module)
    have = config_to_dict(module)
    commands = spec_to_commands(want, have)
    result['commands'] = commands
    if commands:
        commit = (not module.check_mode)
        response = load_config(module, commands, commit=commit)
        result['changed'] = True
    module.exit_json(**result)
