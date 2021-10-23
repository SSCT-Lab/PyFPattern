def add_host(self, host_name, group_ids, status, interfaces, proxy_id, visible_name, description, tls_connect, tls_accept, tls_psk_identity, tls_psk, tls_issuer, tls_subject):
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
        host_list = self._zapi.host.create(parameters)
        if (len(host_list) >= 1):
            return host_list['hostids'][0]
    except Exception as e:
        self._module.fail_json(msg=('Failed to create host %s: %s' % (host_name, e)))