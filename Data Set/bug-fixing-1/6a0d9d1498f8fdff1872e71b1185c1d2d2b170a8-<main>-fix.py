

def main():
    ' main entry point for module execution\n    '
    argument_spec = dict(dest=dict(choices=['console', 'host', 'file', 'user']), name=dict(), facility=dict(), level=dict(), rotate_frequency=dict(type='int'), size=dict(type='int'), files=dict(type='int'), src_addr=dict(), aggregate=dict(), purge=dict(default=False, type='bool'), state=dict(default='present', choices=['present', 'absent']), active=dict(default=True, type='bool'))
    argument_spec.update(junos_argument_spec)
    required_if = [('dest', 'host', ['name', 'facility', 'level']), ('dest', 'file', ['name', 'facility', 'level']), ('dest', 'user', ['name', 'facility', 'level']), ('dest', 'console', ['facility', 'level'])]
    module = AnsibleModule(argument_spec=argument_spec, required_if=required_if, supports_check_mode=True)
    warnings = list()
    check_args(module, warnings)
    result = {
        'changed': False,
    }
    if warnings:
        result['warnings'] = warnings
    dest = module.params.get('dest')
    if ((dest == 'console') and module.params.get('name')):
        module.fail_json(msg=('%s and %s are mutually exclusive' % ('console', 'name')))
    top = 'system/syslog'
    is_facility_key = False
    field_top = None
    if dest:
        if (dest == 'console'):
            field_top = dest
            is_facility_key = True
        else:
            field_top = (dest + '/contents')
            is_facility_key = False
    param_to_xpath_map = collections.OrderedDict()
    param_to_xpath_map.update([('name', {
        'xpath': 'name',
        'is_key': True,
        'top': dest,
    }), ('facility', {
        'xpath': 'name',
        'is_key': is_facility_key,
        'top': field_top,
    }), ('size', {
        'xpath': 'size',
        'leaf_only': True,
        'is_key': True,
        'top': 'archive',
    }), ('files', {
        'xpath': 'files',
        'leaf_only': True,
        'is_key': True,
        'top': 'archive',
    }), ('rotate_frequency', {
        'xpath': 'log-rotate-frequency',
        'leaf_only': True,
    })])
    if module.params.get('level'):
        param_to_xpath_map['level'] = {
            'xpath': module.params.get('level'),
            'tag_only': True,
            'top': field_top,
        }
    validate_param_values(module, param_to_xpath_map)
    want = map_params_to_obj(module, param_to_xpath_map)
    ele = map_obj_to_ele(module, want, top)
    with locked_config(module):
        diff = load_config(module, tostring(ele), warnings, action='replace')
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
