

def main():
    ' main entry point for module execution\n    '
    element_spec = dict(name=dict(), mode=dict(choices=['access', 'trunk']), access_vlan=dict(), native_vlan=dict(type='int'), trunk_vlans=dict(type='list'), unit=dict(default=0, type='int'), description=dict(), state=dict(default='present', choices=['present', 'absent']), active=dict(default=True, type='bool'))
    aggregate_spec = deepcopy(element_spec)
    aggregate_spec['name'] = dict(required=True)
    remove_default_spec(aggregate_spec)
    required_one_of = [['name', 'aggregate']]
    mutually_exclusive = [['name', 'aggregate'], ['access_vlan', 'trunk_vlans'], ['access_vlan', 'native_vlan']]
    required_if = [('mode', 'access', ('access_vlan',)), ('mode', 'trunk', ('trunk_vlans',))]
    argument_spec = dict(aggregate=dict(type='list', elements='dict', options=aggregate_spec, mutually_exclusive=mutually_exclusive, required_if=required_if))
    argument_spec.update(element_spec)
    argument_spec.update(junos_argument_spec)
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True, mutually_exclusive=mutually_exclusive, required_one_of=required_one_of, required_if=required_if)
    warnings = list()
    result = {
        'changed': False,
    }
    if warnings:
        result['warnings'] = warnings
    top = 'interfaces/interface'
    param_to_xpath_map = collections.OrderedDict()
    param_to_xpath_map.update([('name', {
        'xpath': 'name',
        'is_key': True,
    }), ('unit', {
        'xpath': 'name',
        'top': 'unit',
        'is_key': True,
    }), ('mode', {
        'xpath': 'interface-mode',
        'top': 'unit/family/ethernet-switching',
    }), ('access_vlan', {
        'xpath': 'members',
        'top': 'unit/family/ethernet-switching/vlan',
    }), ('trunk_vlans', {
        'xpath': 'members',
        'top': 'unit/family/ethernet-switching/vlan',
    }), ('native_vlan', {
        'xpath': 'native-vlan-id',
    }), ('description', 'description')])
    params = to_param_list(module)
    requests = list()
    for param in params:
        for key in param:
            if (param.get(key) is None):
                param[key] = module.params[key]
        item = param.copy()
        validate_param_values(module, param_to_xpath_map, param=item)
        want = map_params_to_obj(module, param_to_xpath_map, param=item)
        requests.append(map_obj_to_ele(module, want, top, param=item))
    diff = None
    with locked_config(module):
        for req in requests:
            diff = load_config(module, tostring(req), warnings, action='replace')
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
