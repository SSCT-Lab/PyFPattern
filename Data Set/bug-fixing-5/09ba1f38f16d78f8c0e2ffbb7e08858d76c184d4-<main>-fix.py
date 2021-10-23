def main():
    'Main ansible module function\n    '
    module = AnsibleModule(argument_spec=dict(server_url=dict(type='str', required=True, aliases=['url']), login_user=dict(type='str', required=True), login_password=dict(type='str', required=True, no_log=True), http_login_user=dict(type='str', required=False, default=None), http_login_password=dict(type='str', required=False, default=None, no_log=True), validate_certs=dict(type='bool', required=False, default=True), esc_period=dict(type='int', required=False, default=60), timeout=dict(type='int', default=10), name=dict(type='str', required=True), event_source=dict(type='str', required=True, choices=['trigger', 'discovery', 'auto_registration', 'internal']), state=dict(type='str', required=False, default='present', choices=['present', 'absent']), status=dict(type='str', required=False, default='enabled', choices=['enabled', 'disabled']), default_message=dict(type='str', required=False, default=None), default_subject=dict(type='str', required=False, default=None), recovery_default_message=dict(type='str', required=False, default=None), recovery_default_subject=dict(type='str', required=False, default=None), acknowledge_default_message=dict(type='str', required=False, default=None), acknowledge_default_subject=dict(type='str', required=False, default=None), conditions=dict(type='list', required=False, default=None), formula=dict(type='str', required=False, default=None), operations=dict(type='list', required=False, default=None), recovery_operations=dict(type='list', required=False, default=[]), acknowledge_operations=dict(type='list', required=False, default=[])), supports_check_mode=True)
    if (not HAS_ZABBIX_API):
        module.fail_json(msg='Missing required zabbix-api module (check docs or install with: pip install zabbix-api)')
    server_url = module.params['server_url']
    login_user = module.params['login_user']
    login_password = module.params['login_password']
    http_login_user = module.params['http_login_user']
    http_login_password = module.params['http_login_password']
    validate_certs = module.params['validate_certs']
    timeout = module.params['timeout']
    name = module.params['name']
    esc_period = module.params['esc_period']
    event_source = module.params['event_source']
    state = module.params['state']
    status = module.params['status']
    default_message = module.params['default_message']
    default_subject = module.params['default_subject']
    recovery_default_message = module.params['recovery_default_message']
    recovery_default_subject = module.params['recovery_default_subject']
    acknowledge_default_message = module.params['acknowledge_default_message']
    acknowledge_default_subject = module.params['acknowledge_default_subject']
    conditions = module.params['conditions']
    formula = module.params['formula']
    operations = module.params['operations']
    recovery_operations = module.params['recovery_operations']
    acknowledge_operations = module.params['acknowledge_operations']
    try:
        zbx = ZabbixAPI(server_url, timeout=timeout, user=http_login_user, passwd=http_login_password, validate_certs=validate_certs)
        zbx.login(login_user, login_password)
    except Exception as e:
        module.fail_json(msg=('Failed to connect to Zabbix server: %s' % e))
    zapi_wrapper = Zapi(module, zbx)
    action = Action(module, zbx, zapi_wrapper)
    action_exists = zapi_wrapper.check_if_action_exists(name)
    ops = Operations(module, zbx, zapi_wrapper)
    recovery_ops = RecoveryOperations(module, zbx, zapi_wrapper)
    acknowledge_ops = AcknowledgeOperations(module, zbx, zapi_wrapper)
    fltr = Filter(module, zbx, zapi_wrapper)
    if action_exists:
        action_id = zapi_wrapper.get_action_by_name(name)['actionid']
        if (state == 'absent'):
            result = action.delete_action(action_id)
            module.exit_json(changed=True, msg=('Action Deleted: %s, ID: %s' % (name, result)))
        else:
            difference = action.check_difference(action_id=action_id, name=name, event_source=event_source, esc_period=esc_period, status=status, default_message=default_message, default_subject=default_subject, recovery_default_message=recovery_default_message, recovery_default_subject=recovery_default_subject, acknowledge_default_message=acknowledge_default_message, acknowledge_default_subject=acknowledge_default_subject, operations=ops.construct_the_data(operations), recovery_operations=recovery_ops.construct_the_data(recovery_operations), acknowledge_operations=acknowledge_ops.construct_the_data(acknowledge_operations), conditions=fltr.construct_the_data(formula, conditions))
            if (difference == {
                
            }):
                module.exit_json(changed=False, msg=('Action is up to date: %s' % name))
            else:
                result = action.update_action(action_id=action_id, **difference)
                module.exit_json(changed=True, msg=('Action Updated: %s, ID: %s' % (name, result)))
    elif (state == 'absent'):
        module.exit_json(changed=False)
    else:
        action_id = action.add_action(name=name, event_source=event_source, esc_period=esc_period, status=status, default_message=default_message, default_subject=default_subject, recovery_default_message=recovery_default_message, recovery_default_subject=recovery_default_subject, acknowledge_default_message=acknowledge_default_message, acknowledge_default_subject=acknowledge_default_subject, operations=ops.construct_the_data(operations), recovery_operations=recovery_ops.construct_the_data(recovery_operations), acknowledge_operations=acknowledge_ops.construct_the_data(acknowledge_operations), conditions=fltr.construct_the_data(formula, conditions))
        module.exit_json(changed=True, msg=('Action created: %s, ID: %s' % (name, action_id)))