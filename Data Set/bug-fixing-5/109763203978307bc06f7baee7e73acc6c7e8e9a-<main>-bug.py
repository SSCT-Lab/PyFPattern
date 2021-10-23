def main():
    ' main entry point for module execution\n    '
    element_spec = dict(name=dict(type='str', aliases=['interface']), mode=dict(choices=['access', 'trunk']), access_vlan=dict(type='str'), native_vlan=dict(type='str'), trunk_allowed_vlans=dict(type='str', aliases=['trunk_vlans']), state=dict(default='present', choices=['present', 'absent']))
    aggregate_spec = deepcopy(element_spec)
    aggregate_spec['name'] = dict(required=True)
    remove_default_spec(aggregate_spec)
    argument_spec = dict(aggregate=dict(type='list', elements='dict', options=aggregate_spec))
    argument_spec.update(element_spec)
    argument_spec.update(eos_argument_spec)
    module = AnsibleModule(argument_spec=argument_spec, mutually_exclusive=[['access_vlan', 'native_vlan'], ['access_vlan', 'trunk_allowed_vlans']], supports_check_mode=True)
    warnings = list()
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