def main():
    '\n    main entry point for module execution\n    '
    argument_spec = dict(qualifier=dict(required=False, default='target', type='str', choices=['target', 'observed', 'proposed', 'realtime', 'registration', 'running', 'startup']), module_name=dict(required=True, type='str'), attr_type=dict(required=False, type='dict'), attr_data=dict(required=True, type='dict'), operation=dict(required=False, default='create', type='str', choices=['delete', 'create', 'set', 'action', 'get']), db=dict(required=False, default=False, type='bool'), commit_event=dict(required=False, default=False, type='bool'))
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=False)
    if (not HAS_CPS):
        module.fail_json(msg='CPS library required for this module')
    qualifier = module.params['qualifier']
    module_name = module.params['module_name']
    attr_type = module.params['attr_type']
    attr_data = module.params['attr_data']
    operation = module.params['operation']
    db = module.params['db']
    commit_event = module.params['commit_event']
    RESULT = dict(changed=False, db=False, commit_event=False)
    obj = parse_cps_parameters(module_name, qualifier, attr_type, attr_data, operation, db, commit_event)
    if db:
        RESULT['db'] = True
    if commit_event:
        RESULT['commit_event'] = True
    try:
        if (operation == 'get'):
            RESULT.update(cps_get(obj))
        else:
            config = get_config(module)
            diff = attr_data
            if config:
                candidate = dict()
                for (key, val) in iteritems(attr_data):
                    if (key == 'cps/key_data'):
                        candidate.update(val)
                    else:
                        candidate[key] = val
                diff = diff_dict(candidate, config)
            if (operation == 'delete'):
                if config:
                    RESULT.update({
                        'config': config,
                        'candidate': attr_data,
                        'diff': diff,
                    })
                    RESULT.update(cps_transaction(obj))
            elif diff:
                if ('cps/key_data' in attr_data):
                    diff.update(attr_data['cps/key_data'])
                obj = parse_cps_parameters(module_name, qualifier, attr_type, diff, operation, db, commit_event)
                RESULT.update({
                    'config': config,
                    'candidate': attr_data,
                    'diff': diff,
                })
                RESULT.update(cps_transaction(obj))
    except Exception as e:
        module.fail_json(msg=((str(type(e).__name__) + ': ') + str(e)))
    module.exit_json(**RESULT)