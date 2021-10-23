def update_host(self, host_name, group_ids, status, host_id, interfaces, exist_interface_list, proxy_id, visible_name, description, tls_connect, tls_accept, tls_psk_identity, tls_psk, tls_issuer, tls_subject, ipmi_authtype, ipmi_privilege, ipmi_username, ipmi_password):
    try:
        if self._module.check_mode:
            self._module.exit_json(changed=True)
        parameters = {
            'hostid': host_id,
            'groups': group_ids,
            'status': status,
            'tls_connect': tls_connect,
            'tls_accept': tls_accept,
        }
        if (proxy_id >= 0):
            parameters['proxy_hostid'] = proxy_id
        if visible_name:
            parameters['name'] = visible_name
        if tls_psk_identity:
            parameters['tls_psk_identity'] = tls_psk_identity
        if tls_psk:
            parameters['tls_psk'] = tls_psk
        if tls_issuer:
            parameters['tls_issuer'] = tls_issuer
        if tls_subject:
            parameters['tls_subject'] = tls_subject
        if description:
            parameters['description'] = description
        if ipmi_authtype:
            parameters['ipmi_authtype'] = ipmi_authtype
        if ipmi_privilege:
            parameters['ipmi_privilege'] = ipmi_privilege
        if ipmi_username:
            parameters['ipmi_username'] = ipmi_username
        if ipmi_password:
            parameters['ipmi_password'] = ipmi_password
        self._zapi.host.update(parameters)
        interface_list_copy = exist_interface_list
        if interfaces:
            for interface in interfaces:
                flag = False
                interface_str = interface
                for exist_interface in exist_interface_list:
                    interface_type = int(interface['type'])
                    exist_interface_type = int(exist_interface['type'])
                    if (interface_type == exist_interface_type):
                        interface_str['interfaceid'] = exist_interface['interfaceid']
                        self._zapi.hostinterface.update(interface_str)
                        flag = True
                        interface_list_copy.remove(exist_interface)
                        break
                if (not flag):
                    interface_str['hostid'] = host_id
                    self._zapi.hostinterface.create(interface_str)
            remove_interface_ids = []
            for remove_interface in interface_list_copy:
                interface_id = remove_interface['interfaceid']
                remove_interface_ids.append(interface_id)
            if (len(remove_interface_ids) > 0):
                self._zapi.hostinterface.delete(remove_interface_ids)
    except Exception as e:
        self._module.fail_json(msg=('Failed to update host %s: %s' % (host_name, e)))