

def check_all_properties(self, host_id, host_groups, status, interfaces, template_ids, exist_interfaces, host, proxy_id, visible_name, description, host_name, inventory_mode, inventory_zabbix, tls_accept, tls_psk_identity, tls_psk, tls_issuer, tls_subject, tls_connect, ipmi_authtype, ipmi_privilege, ipmi_username, ipmi_password):
    exist_host_groups = self.get_host_groups_by_host_id(host_id)
    if (set(host_groups) != set(exist_host_groups)):
        return True
    exist_status = self.get_host_status_by_host(host)
    if (int(status) != int(exist_status)):
        return True
    if self.check_interface_properties(exist_interfaces, interfaces):
        return True
    exist_template_ids = self.get_host_templates_by_host_id(host_id)
    if (set(list(template_ids)) != set(exist_template_ids)):
        return True
    if (int(host['proxy_hostid']) != int(proxy_id)):
        return True
    if visible_name:
        if ((host['name'] != visible_name) and (host['name'] != host_name)):
            return True
    if description:
        if (host['description'] != description):
            return True
    if inventory_mode:
        if host['inventory']:
            if (int(host['inventory']['inventory_mode']) != self.inventory_mode_numeric(inventory_mode)):
                return True
        elif (inventory_mode != 'disabled'):
            return True
    if inventory_zabbix:
        proposed_inventory = copy.deepcopy(host['inventory'])
        proposed_inventory.update(inventory_zabbix)
        if (proposed_inventory != host['inventory']):
            return True
    if ((tls_accept is not None) and ('tls_accept' in host)):
        if (int(host['tls_accept']) != tls_accept):
            return True
    if ((tls_psk_identity is not None) and ('tls_psk_identity' in host)):
        if (host['tls_psk_identity'] != tls_psk_identity):
            return True
    if ((tls_psk is not None) and ('tls_psk' in host)):
        if (host['tls_psk'] != tls_psk):
            return True
    if ((tls_issuer is not None) and ('tls_issuer' in host)):
        if (host['tls_issuer'] != tls_issuer):
            return True
    if ((tls_subject is not None) and ('tls_subject' in host)):
        if (host['tls_subject'] != tls_subject):
            return True
    if ((tls_connect is not None) and ('tls_connect' in host)):
        if (int(host['tls_connect']) != tls_connect):
            return True
    if (ipmi_authtype is not None):
        if (int(host['ipmi_authtype']) != ipmi_authtype):
            return True
    if (ipmi_privilege is not None):
        if (int(host['ipmi_privilege']) != ipmi_privilege):
            return True
    if (ipmi_username is not None):
        if (host['ipmi_username'] != ipmi_username):
            return True
    if (ipmi_password is not None):
        if (host['ipmi_password'] != ipmi_password):
            return True
    return False
