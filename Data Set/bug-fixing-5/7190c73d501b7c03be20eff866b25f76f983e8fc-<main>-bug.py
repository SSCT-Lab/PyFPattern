def main():
    module = AnsibleModule(argument_spec=dict(server_url=dict(type='str', required=True, aliases=['url']), login_user=dict(type='str', required=True), login_password=dict(type='str', required=True, no_log=True), http_login_user=dict(type='str', required=False, default=None), http_login_password=dict(type='str', required=False, default=None, no_log=True), validate_certs=dict(type='bool', required=False, default=True), host_name=dict(type='str', required=True), macro_name=dict(type='str', required=True), macro_value=dict(type='str', required=True), state=dict(default='present', choices=['present', 'absent']), timeout=dict(type='int', default=10), force=dict(type='bool', default=True)), supports_check_mode=True)
    if (not HAS_ZABBIX_API):
        module.fail_json(msg='Missing required zabbix-api module (check docs or install with: pip install zabbix-api)')
    server_url = module.params['server_url']
    login_user = module.params['login_user']
    login_password = module.params['login_password']
    http_login_user = module.params['http_login_user']
    http_login_password = module.params['http_login_password']
    validate_certs = module.params['validate_certs']
    host_name = module.params['host_name']
    macro_name = module.params['macro_name'].upper()
    macro_value = module.params['macro_value']
    state = module.params['state']
    timeout = module.params['timeout']
    force = module.params['force']
    zbx = None
    try:
        zbx = ZabbixAPIExtends(server_url, timeout=timeout, user=http_login_user, passwd=http_login_password, validate_certs=validate_certs)
        zbx.login(login_user, login_password)
    except Exception as e:
        module.fail_json(msg=('Failed to connect to Zabbix server: %s' % e))
    host_macro_class_obj = HostMacro(module, zbx)
    if host_name:
        host_id = host_macro_class_obj.get_host_id(host_name)
        host_macro_obj = host_macro_class_obj.get_host_macro(macro_name, host_id)
    if (state == 'absent'):
        if (not host_macro_obj):
            module.exit_json(changed=False, msg=('Host Macro %s does not exist' % macro_name))
        else:
            host_macro_class_obj.delete_host_macro(host_macro_obj, macro_name)
    elif (not host_macro_obj):
        host_macro_class_obj.create_host_macro(macro_name, macro_value, host_id)
    elif force:
        host_macro_class_obj.update_host_macro(host_macro_obj, macro_name, macro_value)
    else:
        module.exit_json(changed=False, result=('Host macro %s already exists and force is set to no' % macro_name))