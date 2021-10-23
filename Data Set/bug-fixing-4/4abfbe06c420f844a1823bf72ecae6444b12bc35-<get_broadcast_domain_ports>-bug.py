def get_broadcast_domain_ports(self):
    '\n        Return details about the broadcast domain ports\n        :param:\n            name : broadcast domain name\n        :return: Details about the broadcast domain. None if not found.\n        :rtype: dict\n        '
    domain_get_iter = netapp_utils.zapi.NaElement('net-port-broadcast-domain-get-iter')
    broadcast_domain_info = netapp_utils.zapi.NaElement('net-port-broadcast-domain-info')
    broadcast_domain_info.add_new_child('broadcast-domain', self.broadcast_domain)
    query = netapp_utils.zapi.NaElement('query')
    query.add_child_elem(broadcast_domain_info)
    domain_get_iter.add_child_elem(query)
    result = self.server.invoke_successfully(domain_get_iter, True)
    domain_exists = None
    if (result.get_child_by_name('num-records') and (int(result.get_child_content('num-records')) == 1)):
        domain_info = result.get_child_by_name('attributes-list').get_child_by_name('net-port-broadcast-domain-info')
        domain_name = domain_info.get_child_content('broadcast-domain')
        domain_ports = domain_info.get_child_content('port-info')
        domain_exists = {
            'domain-name': domain_name,
            'ports': domain_ports,
        }
    return domain_exists