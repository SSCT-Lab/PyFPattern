

def main():
    ' main entry point for module execution\n    '
    element_spec = dict(name=dict(), full_name=dict(), role=dict(choices=ROLES), encrypted_password=dict(), sshkey=dict(), state=dict(choices=['present', 'absent'], default='present'), active=dict(type='bool', default=True))
    aggregate_spec = deepcopy(element_spec)
    aggregate_spec['name'] = dict(required=True)
    remove_default_spec(aggregate_spec)
    argument_spec = dict(aggregate=dict(type='list', elements='dict', options=aggregate_spec, aliases=['collection', 'users']), purge=dict(default=False, type='bool'))
    argument_spec.update(element_spec)
    argument_spec.update(junos_argument_spec)
    mutually_exclusive = [['aggregate', 'name']]
    module = AnsibleModule(argument_spec=argument_spec, mutually_exclusive=mutually_exclusive, supports_check_mode=True)
    warnings = list()
    result = {
        'changed': False,
        'warnings': warnings,
    }
    want = map_params_to_obj(module)
    ele = map_obj_to_ele(module, want)
    purge_request = None
    if module.params['purge']:
        purge_request = handle_purge(module, want)
    with locked_config(module):
        if purge_request:
            load_config(module, tostring(purge_request), warnings, action='replace')
        diff = load_config(module, tostring(ele), warnings, action='merge')
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
