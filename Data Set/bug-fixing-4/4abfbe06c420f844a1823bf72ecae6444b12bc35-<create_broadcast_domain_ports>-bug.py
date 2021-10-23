def create_broadcast_domain_ports(self):
    '\n        Creates new broadcast domain ports\n        '
    domain_obj = netapp_utils.zapi.NaElement('net-port-broadcast-domain-add-ports')
    domain_obj.add_new_child('broadcast-domain', self.broadcast_domain)
    if self.ipspace:
        domain_obj.add_new_child('ipspace', self.ipspace)
    if self.ports:
        ports_obj = netapp_utils.zapi.NaElement('ports')
        domain_obj.add_child_elem(ports_obj)
        for port in self.ports:
            ports_obj.add_new_child('net-qualified-port-name', port)
    try:
        self.server.invoke_successfully(domain_obj, True)
        return True
    except netapp_utils.zapi.NaApiError as error:
        if (to_native(error.code) == '18605'):
            return False
        else:
            self.module.fail_json(msg=('Error creating port for broadcast domain %s: %s' % (self.broadcast_domain, to_native(error))), exception=traceback.format_exc())