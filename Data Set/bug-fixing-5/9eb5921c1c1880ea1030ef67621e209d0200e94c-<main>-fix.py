def main():
    ' main entry point for module execution\n    '
    element_spec = dict(address=dict(type='str', aliases=['prefix']), next_hop=dict(type='str'), admin_distance=dict(default=1, type='int'), state=dict(default='present', choices=['present', 'absent']))
    aggregate_spec = deepcopy(element_spec)
    aggregate_spec['address'] = dict(required=True)
    remove_default_spec(aggregate_spec)
    argument_spec = dict(aggregate=dict(type='list', elements='dict', options=aggregate_spec))
    argument_spec.update(element_spec)
    argument_spec.update(eos_argument_spec)
    required_one_of = [['aggregate', 'address']]
    required_together = [['address', 'next_hop']]
    mutually_exclusive = [['aggregate', 'address']]
    module = AnsibleModule(argument_spec=argument_spec, required_one_of=required_one_of, required_together=required_together, mutually_exclusive=mutually_exclusive, supports_check_mode=True)
    address = module.params['address']
    if (address is not None):
        prefix = address.split('/')[(- 1)]
    if (address and prefix):
        if (('/' not in address) or (not validate_ip_address(address.split('/')[0]))):
            module.fail_json(msg='{} is not a valid IP address'.format(address))
        if (not validate_prefix(prefix)):
            module.fail_json(msg='Length of prefix should be between 0 and 32 bits')
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