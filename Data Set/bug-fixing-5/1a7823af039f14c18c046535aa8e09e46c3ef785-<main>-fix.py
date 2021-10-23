def main():
    module = AnsibleModule(argument_spec=dict(server_url=dict(type='str', required=True, aliases=['url']), login_user=dict(type='str', required=True), login_password=dict(type='str', required=True, no_log=True), http_login_user=dict(type='str', required=False, default=None), http_login_password=dict(type='str', required=False, default=None, no_log=True), validate_certs=dict(type='bool', required=False, default=True), alias=dict(type='str', required=True), timeout=dict(type='int', default=10)), supports_check_mode=True)
    if (not HAS_ZABBIX_API):
        module.fail_json(msg=missing_required_lib('zabbix-api', url='https://pypi.org/project/zabbix-api/'), exception=ZBX_IMP_ERR)
    server_url = module.params['server_url']
    login_user = module.params['login_user']
    login_password = module.params['login_password']
    http_login_user = module.params['http_login_user']
    http_login_password = module.params['http_login_password']
    validate_certs = module.params['validate_certs']
    alias = module.params['alias']
    timeout = module.params['timeout']
    zbx = None
    try:
        zbx = ZabbixAPI(server_url, timeout=timeout, user=http_login_user, passwd=http_login_password, validate_certs=validate_certs)
        zbx.login(login_user, login_password)
        atexit.register(zbx.logout)
    except Exception as e:
        module.fail_json(msg=('Failed to connect to Zabbix server: %s' % e))
    user = User(module, zbx)
    zabbix_user = user.get_user_by_user_alias(alias)
    zbx.logout()
    module.exit_json(changed=False, zabbix_user=zabbix_user)