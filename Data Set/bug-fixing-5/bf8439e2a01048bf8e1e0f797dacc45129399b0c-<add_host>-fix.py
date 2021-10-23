def add_host(self, host_name, group_ids, status, interfaces, proxy_id, visible_name, description, tls_connect, tls_accept, tls_psk_identity, tls_psk, tls_issuer, tls_subject, ipmi_authtype, ipmi_privilege, ipmi_username, ipmi_password):
    try:
        if self._module.check_mode:
            self._module.exit_json(changed=True)
        parameters = {
            'host': host_name,
            'interfaces': interfaces,
            'groups': group_ids,
            'status': status,
            'tls_connect': tls_connect,
            'tls_accept': tls_accept,
        }
        if proxy_id:
            parameters['proxy_hostid'] = proxy_id
        if visible_name:
            parameters['name'] = visible_name
        if (tls_psk_identity is not None):
            parameters['tls_psk_identity'] = tls_psk_identity
        if (tls_psk is not None):
            parameters['tls_psk'] = tls_psk
        if (tls_issuer is not None):
            parameters['tls_issuer'] = tls_issuer
        if (tls_subject is not None):
            parameters['tls_subject'] = tls_subject
        if description:
            parameters['description'] = description
        if (ipmi_authtype is not None):
            parameters['ipmi_authtype'] = ipmi_authtype
        if (ipmi_privilege is not None):
            parameters['ipmi_privilege'] = ipmi_privilege
        if (ipmi_username is not None):
            parameters['ipmi_username'] = ipmi_username
        if (ipmi_password is not None):
            parameters['ipmi_password'] = ipmi_password
        host_list = self._zapi.host.create(parameters)
        if (len(host_list) >= 1):
            return host_list['hostids'][0]
    except Exception as e:
        self._module.fail_json(msg=('Failed to create host %s: %s' % (host_name, e)))