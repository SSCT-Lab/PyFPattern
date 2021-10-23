def main():
    ' main entry point for module execution\n    '
    element_spec = dict(prefix=dict(type='str'), mask=dict(type='str'), next_hop=dict(type='str'), vrf=dict(type='str'), interface=dict(type='str'), name=dict(type='str', aliases=['description']), admin_distance=dict(type='str'), track=dict(type='str'), tag=dict(tag='str'), state=dict(default='present', choices=['present', 'absent']))
    aggregate_spec = deepcopy(element_spec)
    aggregate_spec['prefix'] = dict(required=True)
    remove_default_spec(aggregate_spec)
    argument_spec = dict(aggregate=dict(type='list', elements='dict', options=aggregate_spec))
    argument_spec.update(element_spec)
    argument_spec.update(ios_argument_spec)
    required_one_of = [['aggregate', 'prefix']]
    required_together = [['prefix', 'mask']]
    mutually_exclusive = [['aggregate', 'prefix']]
    module = AnsibleModule(argument_spec=argument_spec, required_one_of=required_one_of, mutually_exclusive=mutually_exclusive, supports_check_mode=True)
    warnings = list()
    check_args(module, warnings)
    result = {
        'changed': False,
    }
    if warnings:
        result['warnings'] = warnings
    want = map_params_to_obj(module, required_together=required_together)
    have = map_config_to_obj(module)
    commands = map_obj_to_commands(want, have)
    result['commands'] = commands
    if commands:
        if (not module.check_mode):
            load_config(module, commands)
        result['changed'] = True
    module.exit_json(**result)