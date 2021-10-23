def main():
    module = AnsibleModule(argument_spec=dict(server_url=dict(type='str', required=True, aliases=['url']), login_user=dict(type='str', required=True), login_password=dict(type='str', required=True, no_log=True), host_name=dict(type='str', required=True), http_login_user=dict(type='str', required=False, default=None), http_login_password=dict(type='str', required=False, default=None, no_log=True), host_groups=dict(type='list', required=False), link_templates=dict(type='list', required=False), status=dict(default='enabled', choices=['enabled', 'disabled']), state=dict(default='present', choices=['present', 'absent']), inventory_mode=dict(required=False, choices=['automatic', 'manual', 'disabled']), tls_connect=dict(type='int', default=1), tls_accept=dict(type='int', default=1), tls_psk_identity=dict(type='str', required=False), tls_psk=dict(type='str', required=False), tls_issuer=dict(type='str', required=False), tls_subject=dict(type='str', required=False), timeout=dict(type='int', default=10), interfaces=dict(type='list', required=False), force=dict(type='bool', default=True), proxy=dict(type='str', required=False), visible_name=dict(type='str', required=False)), supports_check_mode=True)
    if (not HAS_ZABBIX_API):
        module.fail_json(msg='Missing required zabbix-api module (check docs or install with: pip install zabbix-api)')
    server_url = module.params['server_url']
    login_user = module.params['login_user']
    login_password = module.params['login_password']
    http_login_user = module.params['http_login_user']
    http_login_password = module.params['http_login_password']
    host_name = module.params['host_name']
    visible_name = module.params['visible_name']
    host_groups = module.params['host_groups']
    link_templates = module.params['link_templates']
    inventory_mode = module.params['inventory_mode']
    tls_connect = module.params['tls_connect']
    tls_accept = module.params['tls_accept']
    tls_psk_identity = module.params['tls_psk_identity']
    tls_psk = module.params['tls_psk']
    tls_issuer = module.params['tls_issuer']
    tls_subject = module.params['tls_subject']
    status = module.params['status']
    state = module.params['state']
    timeout = module.params['timeout']
    interfaces = module.params['interfaces']
    force = module.params['force']
    proxy = module.params['proxy']
    status = (1 if (status == 'disabled') else 0)
    zbx = None
    try:
        zbx = ZabbixAPIExtends(server_url, timeout=timeout, user=http_login_user, passwd=http_login_password)
        zbx.login(login_user, login_password)
    except Exception as e:
        module.fail_json(msg=('Failed to connect to Zabbix server: %s' % e))
    host = Host(module, zbx)
    template_ids = []
    if link_templates:
        template_ids = host.get_template_ids(link_templates)
    group_ids = []
    if host_groups:
        group_ids = host.get_group_ids_by_group_names(host_groups)
    ip = ''
    if interfaces:
        for interface in interfaces:
            if (interface['type'] == 1):
                ip = interface['ip']
    is_host_exist = host.is_host_exist(host_name)
    if is_host_exist:
        if proxy:
            proxy_id = host.get_proxyid_by_proxy_name(proxy)
        else:
            proxy_id = 0
        zabbix_host_obj = host.get_host_by_host_name(host_name)
        host_id = zabbix_host_obj['hostid']
        if (state == 'absent'):
            host.delete_host(host_id, host_name)
            module.exit_json(changed=True, result=('Successfully delete host %s' % host_name))
        else:
            if (not group_ids):
                module.fail_json(msg=("Specify at least one group for updating host '%s'." % host_name))
            if (not force):
                for group_id in host.get_group_ids_by_group_names(host.get_host_groups_by_host_id(host_id)):
                    if (group_id not in group_ids):
                        group_ids.append(group_id)
                for interface in host._zapi.hostinterface.get({
                    'output': 'extend',
                    'hostids': host_id,
                }):
                    for key in interface.keys():
                        if (key in ['interfaceid', 'hostid', 'bulk']):
                            interface.pop(key, None)
                    for index in interface.keys():
                        if (index in ['useip', 'main', 'type', 'port']):
                            interface[index] = int(interface[index])
                    if (interface not in interfaces):
                        interfaces.append(interface)
                template_ids = list(set((template_ids + host.get_host_templates_by_host_id(host_id))))
            exist_interfaces = host._zapi.hostinterface.get({
                'output': 'extend',
                'hostids': host_id,
            })
            exist_interfaces_copy = copy.deepcopy(exist_interfaces)
            interfaces_len = (len(interfaces) if interfaces else 0)
            if (len(exist_interfaces) > interfaces_len):
                if host.check_all_properties(host_id, host_groups, status, interfaces, template_ids, exist_interfaces, zabbix_host_obj, proxy_id, visible_name):
                    host.link_or_clear_template(host_id, template_ids, tls_connect, tls_accept, tls_psk_identity, tls_psk, tls_issuer, tls_subject)
                    host.update_host(host_name, group_ids, status, host_id, interfaces, exist_interfaces, proxy_id, visible_name, tls_connect, tls_accept, tls_psk_identity, tls_psk, tls_issuer, tls_subject)
                    module.exit_json(changed=True, result=("Successfully update host %s (%s) and linked with template '%s'" % (host_name, ip, link_templates)))
                else:
                    module.exit_json(changed=False)
            elif host.check_all_properties(host_id, host_groups, status, interfaces, template_ids, exist_interfaces_copy, zabbix_host_obj, proxy_id, visible_name):
                host.update_host(host_name, group_ids, status, host_id, interfaces, exist_interfaces, proxy_id, visible_name, tls_connect, tls_accept, tls_psk_identity, tls_psk, tls_issuer, tls_subject)
                host.link_or_clear_template(host_id, template_ids, tls_connect, tls_accept, tls_psk_identity, tls_psk, tls_issuer, tls_subject)
                host.update_inventory_mode(host_id, inventory_mode)
                module.exit_json(changed=True, result=("Successfully update host %s (%s) and linked with template '%s'" % (host_name, ip, link_templates)))
            else:
                module.exit_json(changed=False)
    else:
        if (state == 'absent'):
            module.exit_json(changed=False)
        if proxy:
            proxy_id = host.get_proxyid_by_proxy_name(proxy)
        else:
            proxy_id = 0
        if (not group_ids):
            module.fail_json(msg=("Specify at least one group for creating host '%s'." % host_name))
        if ((not interfaces) or (interfaces and (len(interfaces) == 0))):
            module.fail_json(msg=("Specify at least one interface for creating host '%s'." % host_name))
        host_id = host.add_host(host_name, group_ids, status, interfaces, proxy_id, visible_name, tls_connect, tls_accept, tls_psk_identity, tls_psk, tls_issuer, tls_subject)
        host.link_or_clear_template(host_id, template_ids, tls_connect, tls_accept, tls_psk_identity, tls_psk, tls_issuer, tls_subject)
        host.update_inventory_mode(host_id, inventory_mode)
        module.exit_json(changed=True, result=("Successfully added host %s (%s) and linked with template '%s'" % (host_name, ip, link_templates)))