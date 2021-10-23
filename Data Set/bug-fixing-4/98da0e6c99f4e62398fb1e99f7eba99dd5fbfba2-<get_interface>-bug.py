def get_interface(self, interface_name=None):
    '\n        Return details about the interface\n        :param:\n            name : Name of the name of the interface\n\n        :return: Details about the interface. None if not found.\n        :rtype: dict\n        '
    if (interface_name is None):
        interface_name = self.parameters['interface_name']
    interface_info = netapp_utils.zapi.NaElement('net-interface-get-iter')
    interface_attributes = netapp_utils.zapi.NaElement('net-interface-info')
    interface_attributes.add_new_child('interface-name', interface_name)
    query = netapp_utils.zapi.NaElement('query')
    query.add_child_elem(interface_attributes)
    interface_info.add_child_elem(query)
    result = self.server.invoke_successfully(interface_info, True)
    return_value = None
    if (result.get_child_by_name('num-records') and (int(result.get_child_content('num-records')) >= 1)):
        interface_attributes = result.get_child_by_name('attributes-list').get_child_by_name('net-interface-info')
        return_value = {
            'interface_name': self.parameters['interface_name'],
            'admin_status': interface_attributes['administrative-status'],
            'home_port': interface_attributes['home-port'],
            'home_node': interface_attributes['home-node'],
            'failover_policy': interface_attributes['failover-policy'].replace('_', '-'),
            'is_auto_revert': (True if (interface_attributes['is-auto-revert'] == 'true') else False),
        }
        if interface_attributes.get_child_by_name('address'):
            return_value['address'] = interface_attributes['address']
        if interface_attributes.get_child_by_name('netmask'):
            return_value['netmask'] = interface_attributes['netmask']
        if interface_attributes.get_child_by_name('firewall-policy'):
            return_value['firewall_policy'] = interface_attributes['firewall-policy']
    return return_value