

def main():
    module = AnsibleModule(argument_spec=dict(server_url=dict(type='str', required=True, aliases=['url']), login_user=dict(type='str', required=True), login_password=dict(type='str', required=True, no_log=True), proxy_name=dict(type='str', required=True), http_login_user=dict(type='str', required=False, default=None), http_login_password=dict(type='str', required=False, default=None, no_log=True), validate_certs=dict(type='bool', required=False, default=True), status=dict(default='active', choices=['active', 'passive']), state=dict(default='present', choices=['present', 'absent']), description=dict(type='str', required=False), tls_connect=dict(default='no_encryption', choices=['no_encryption', 'PSK', 'certificate']), tls_accept=dict(default='no_encryption', choices=['no_encryption', 'PSK', 'certificate']), tls_issuer=dict(type='str', required=False, default=None), tls_subject=dict(type='str', required=False, default=None), tls_psk_identity=dict(type='str', required=False, default=None), tls_psk=dict(type='str', required=False, default=None), timeout=dict(type='int', default=10), interface=dict(type='dict', required=False, default={
        
    })), supports_check_mode=True)
    if (not HAS_ZABBIX_API):
        module.fail_json(msg=(('Missing required zabbix-api module' + ' (check docs or install with:') + ' pip install zabbix-api)'))
    server_url = module.params['server_url']
    login_user = module.params['login_user']
    login_password = module.params['login_password']
    http_login_user = module.params['http_login_user']
    http_login_password = module.params['http_login_password']
    validate_certs = module.params['validate_certs']
    proxy_name = module.params['proxy_name']
    description = module.params['description']
    status = module.params['status']
    tls_connect = module.params['tls_connect']
    tls_accept = module.params['tls_accept']
    tls_issuer = module.params['tls_issuer']
    tls_subject = module.params['tls_subject']
    tls_psk_identity = module.params['tls_psk_identity']
    tls_psk = module.params['tls_psk']
    state = module.params['state']
    timeout = module.params['timeout']
    interface = module.params['interface']
    status = (6 if (status == 'passive') else 5)
    if (tls_connect == 'certificate'):
        tls_connect = 4
    elif (tls_connect == 'PSK'):
        tls_connect = 2
    else:
        tls_connect = 1
    if (tls_accept == 'certificate'):
        tls_accept = 4
    elif (tls_accept == 'PSK'):
        tls_accept = 2
    else:
        tls_accept = 1
    zbx = None
    try:
        zbx = ZabbixAPI(server_url, timeout=timeout, user=http_login_user, passwd=http_login_password, validate_certs=validate_certs)
        zbx.login(login_user, login_password)
    except Exception as e:
        module.fail_json(msg=('Failed to connect to Zabbix server: %s' % e))
    proxy = Proxy(module, zbx)
    proxy_id = proxy.proxy_exists(proxy_name)
    if proxy_id:
        if (state == 'absent'):
            proxy.delete_proxy(proxy_id, proxy_name)
        else:
            proxy.update_proxy(proxy_id, {
                'host': proxy_name,
                'description': description,
                'status': str(status),
                'tls_connect': str(tls_connect),
                'tls_accept': str(tls_accept),
                'tls_issuer': tls_issuer,
                'tls_subject': tls_subject,
                'tls_psk_identity': tls_psk_identity,
                'tls_psk': tls_psk,
                'interface': interface,
            })
    else:
        if (state == 'absent'):
            module.exit_json(changed=False)
        proxy_id = proxy.add_proxy(data={
            'host': proxy_name,
            'description': description,
            'status': str(status),
            'tls_connect': str(tls_connect),
            'tls_accept': str(tls_accept),
            'tls_issuer': tls_issuer,
            'tls_subject': tls_subject,
            'tls_psk_identity': tls_psk_identity,
            'tls_psk': tls_psk,
            'interface': interface,
        })
