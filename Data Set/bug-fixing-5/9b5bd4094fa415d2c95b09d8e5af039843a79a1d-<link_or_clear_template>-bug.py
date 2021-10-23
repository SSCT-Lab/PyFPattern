def link_or_clear_template(self, host_id, template_id_list, tls_connect, tls_accept, tls_psk_identity, tls_psk, tls_issuer, tls_subject):
    exist_template_id_list = self.get_host_templates_by_host_id(host_id)
    exist_template_ids = set(exist_template_id_list)
    template_ids = set(template_id_list)
    template_id_list = list(template_ids)
    templates_clear = exist_template_ids.difference(template_ids)
    templates_clear_list = list(templates_clear)
    request_str = {
        'hostid': host_id,
        'templates': template_id_list,
        'templates_clear': templates_clear_list,
        'tls_connect': tls_connect,
        'tls_accept': tls_accept,
    }
    if tls_psk_identity:
        request_str['tls_psk_identity'] = tls_psk_identity
    if tls_psk:
        request_str['tls_psk'] = tls_psk
    if tls_issuer:
        request_str['tls_issuer'] = tls_issuer
    if tls_subject:
        request_str['tls_subject'] = tls_subject
    try:
        if self._module.check_mode:
            self._module.exit_json(changed=True)
        self._zapi.host.update(request_str)
    except Exception as e:
        self._module.fail_json(msg=('Failed to link template to host: %s' % e))