def main():
    ' main entry point for module execution\n    '
    element_spec = dict(name=dict(), description=dict(), rd=dict(type='list'), interfaces=dict(type='list'), target=dict(type='list'), state=dict(default='present', choices=['present', 'absent']), active=dict(default=True, type='bool'), table_label=dict(default=True, type='bool'))
    aggregate_spec = deepcopy(element_spec)
    aggregate_spec['name'] = dict(required=True)
    remove_default_spec(aggregate_spec)
    argument_spec = dict(aggregate=dict(type='list', elements='dict', options=aggregate_spec))
    argument_spec.update(element_spec)
    argument_spec.update(junos_argument_spec)
    required_one_of = [['aggregate', 'name']]
    mutually_exclusive = [['aggregate', 'name']]
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True, required_one_of=required_one_of, mutually_exclusive=mutually_exclusive)
    warnings = list()
    check_args(module, warnings)
    result = {
        'changed': False,
    }
    if warnings:
        result['warnings'] = warnings
    top = 'routing-instances/instance'
    param_to_xpath_map = collections.OrderedDict()
    param_to_xpath_map.update([('name', {
        'xpath': 'name',
        'is_key': True,
    }), ('description', 'description'), ('type', 'instance-type'), ('rd', 'route-distinguisher/rd-type'), ('interfaces', 'interface/name'), ('target', 'vrf-target/community'), ('table_label', {
        'xpath': 'vrf-table-label',
        'tag_only': True,
    })])
    params = to_param_list(module)
    requests = list()
    for param in params:
        for key in param:
            if (param.get(key) is None):
                param[key] = module.params[key]
        item = param.copy()
        item['type'] = 'vrf'
        want = map_params_to_obj(module, param_to_xpath_map, param=item)
        requests.append(map_obj_to_ele(module, want, top, param=item))
    with locked_config(module):
        for req in requests:
            diff = load_config(module, tostring(req), warnings, action='merge')
        commit = (not module.check_mode)
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