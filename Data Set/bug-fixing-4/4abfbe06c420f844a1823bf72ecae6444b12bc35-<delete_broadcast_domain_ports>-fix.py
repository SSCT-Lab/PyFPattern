def delete_broadcast_domain_ports(self, ports):
    '\n        Deletes broadcast domain ports\n        '
    domain_obj = netapp_utils.zapi.NaElement('net-port-broadcast-domain-remove-ports')
    domain_obj.add_new_child('broadcast-domain', self.broadcast_domain)
    if self.ipspace:
        domain_obj.add_new_child('ipspace', self.ipspace)
    if ports:
        ports_obj = netapp_utils.zapi.NaElement('ports')
        domain_obj.add_child_elem(ports_obj)
        for port in ports:
            ports_obj.add_new_child('net-qualified-port-name', port)
    try:
        self.server.invoke_successfully(domain_obj, True)
        return True
    except netapp_utils.zapi.NaApiError as error:
        self.module.fail_json(msg=('Error deleting port for broadcast domain %s: %s' % (self.broadcast_domain, to_native(error))), exception=traceback.format_exc())