def get_service_processor_network(self):
    '\n        Return details about service processor network\n        :param:\n            name : name of the vserver\n        :return: Details about service processor network. None if not found.\n        :rtype: dict\n        '
    spn_get_iter = netapp_utils.zapi.NaElement('service-processor-network-get-iter')
    spn_info = netapp_utils.zapi.NaElement('service-processor-network-info')
    spn_info.add_new_child('node', self.node)
    spn_info.add_new_child('address-type', self.address_type)
    spn_info.add_new_child('is-enabled', self.is_enabled)
    query = netapp_utils.zapi.NaElement('query')
    query.add_child_elem(spn_info)
    spn_get_iter.add_child_elem(query)
    result = self.server.invoke_successfully(spn_get_iter, True)
    sp_network_details = None
    if (result.get_child_by_name('num-records') and (int(result.get_child_content('num-records')) >= 1)):
        attributes_list = result.get_child_by_name('attributes-list').get_child_by_name('service-processor-network-info')
        node_value = attributes_list.get_child_content('node')
        address_type_value = attributes_list.get_child_content('address-type')
        dhcp_value = attributes_list.get_child_content('dhcp')
        gateway_ip_address_value = attributes_list.get_child_content('gateway-ip-address')
        ip_address_value = attributes_list.get_child_content('ip-address')
        is_enabled_value = attributes_list.get_child_content('is-enabled')
        netmask_value = attributes_list.get_child_content('netmask')
        prefix_length_value = attributes_list.get_child_content('prefix-length')
        sp_network_details = {
            'node_value': node_value,
            'address_type_value': address_type_value,
            'dhcp_value': dhcp_value,
            'gateway_ip_address_value': gateway_ip_address_value,
            'ip_address_value': ip_address_value,
            'is_enabled_value': is_enabled_value,
            'netmask_value': netmask_value,
            'prefix_length_value': prefix_length_value,
        }
    return sp_network_details