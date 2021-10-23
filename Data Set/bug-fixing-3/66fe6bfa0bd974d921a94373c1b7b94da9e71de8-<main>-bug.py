def main():
    ' main entry point for module execution\n    '
    element_spec = dict(group=dict(type='int'), mode=dict(required=False, choices=['on', 'active', 'passive'], default='on', type='str'), min_links=dict(required=False, default=None, type='int'), members=dict(required=False, default=None, type='list'), force=dict(required=False, default=False, type='bool'), state=dict(required=False, choices=['absent', 'present'], default='present'))
    aggregate_spec = deepcopy(element_spec)
    aggregate_spec['group'] = dict(required=True)
    remove_default_spec(aggregate_spec)
    argument_spec = dict(aggregate=dict(type='list', elements='dict', options=aggregate_spec), purge=dict(default=False, type='bool'))
    argument_spec.update(element_spec)
    argument_spec.update(nxos_argument_spec)
    required_one_of = [['group', 'aggregate']]
    mutually_exclusive = [['group', 'aggregate']]
    module = AnsibleModule(argument_spec=argument_spec, required_one_of=required_one_of, mutually_exclusive=mutually_exclusive, supports_check_mode=True)
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
        if (not module.check_mode):
            resp = load_config(module, commands, True)
            if resp:
                for item in resp:
                    if item:
                        if isinstance(item, dict):
                            err_str = item['clierror']
                        else:
                            err_str = item
                        if ('cannot add' in err_str.lower()):
                            module.fail_json(msg=err_str)
        result['changed'] = True
    module.exit_json(**result)