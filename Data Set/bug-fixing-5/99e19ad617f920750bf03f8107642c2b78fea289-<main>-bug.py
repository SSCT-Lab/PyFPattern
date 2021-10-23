def main():
    module = AnsibleModule(argument_spec=dict(name=dict(required=True), type=dict(required=True, choices=['account', 'auth', 'password', 'session']), control=dict(required=True), module_path=dict(required=True), new_type=dict(required=False, choices=['account', 'auth', 'password', 'session']), new_control=dict(required=False), new_module_path=dict(required=False), module_arguments=dict(required=False), state=dict(required=False, default='updated', choices=['before', 'after', 'updated', 'args_absent', 'args_present']), path=dict(required=False, default='/etc/pam.d')), supports_check_mode=True)
    service = module.params['name']
    old_type = module.params['type']
    old_control = module.params['control']
    old_module_path = module.params['module_path']
    new_type = module.params['new_type']
    new_control = module.params['new_control']
    new_module_path = module.params['new_module_path']
    module_arguments = module.params['module_arguments']
    state = module.params['state']
    path = module.params['path']
    pamd = PamdService(path, service, module)
    old_rule = PamdRule(old_type, old_control, old_module_path)
    new_rule = PamdRule(new_type, new_control, new_module_path, module_arguments)
    try:
        if (state == 'updated'):
            (change, result) = update_rule(pamd, old_rule, new_rule)
        elif (state == 'before'):
            if ((new_rule.rule_control is None) or (new_rule.rule_type is None) or (new_rule.rule_module_path is None)):
                module.fail_json(msg=((('When inserting a new rule before ' + 'or after an existing rule, new_type, ') + 'new_control and new_module_path must ') + 'all be set.'))
            (change, result) = insert_before_rule(pamd, old_rule, new_rule)
        elif (state == 'after'):
            if ((new_rule.rule_control is None) or (new_rule.rule_type is None) or (new_rule.rule_module_path is None)):
                module.fail_json(msg=((('When inserting a new rule before' + 'or after an existing rule, new_type,') + ' new_control and new_module_path must') + ' all be set.'))
            (change, result) = insert_after_rule(pamd, old_rule, new_rule)
        elif (state == 'args_absent'):
            (change, result) = remove_module_arguments(pamd, old_rule, module_arguments)
        elif (state == 'args_present'):
            (change, result) = add_module_arguments(pamd, old_rule, module_arguments)
        if (not module.check_mode):
            write_rules(pamd)
    except Exception:
        e = get_exception()
        module.fail_json(msg=('error running changing pamd: %s' % str(e)))
    facts = {
        
    }
    facts['pamd'] = {
        'changed': change,
        'result': result,
    }
    module.params['dest'] = pamd.fname
    module.exit_json(changed=change, ansible_facts=facts)