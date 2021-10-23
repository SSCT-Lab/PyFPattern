def get_vserver(self):
    '\n        Checks if vserver exists.\n\n        :return:\n            True if vserver found\n            False if vserver is not found\n        :rtype: bool\n        '
    vserver_info = netapp_utils.zapi.NaElement('vserver-get-iter')
    query_details = netapp_utils.zapi.NaElement.create_node_with_children('vserver-info', **{
        'vserver-name': self.name,
    })
    query = netapp_utils.zapi.NaElement('query')
    query.add_child_elem(query_details)
    vserver_info.add_child_elem(query)
    result = self.server.invoke_successfully(vserver_info, enable_tunneling=False)
    vserver_details = None
    if (result.get_child_by_name('num-records') and (int(result.get_child_content('num-records')) >= 1)):
        attributes_list = result.get_child_by_name('attributes-list')
        vserver_info = attributes_list.get_child_by_name('vserver-info')
        aggr_list = list()
        ' vserver aggr-list can be empty by default'
        get_list = vserver_info.get_child_by_name('aggr-list')
        if (get_list is not None):
            aggregates = get_list.get_children()
            for aggr in aggregates:
                aggr_list.append(aggr.get_content())
        protocols = list()
        'allowed-protocols is not empty by default'
        get_protocols = vserver_info.get_child_by_name('allowed-protocols').get_children()
        for protocol in get_protocols:
            protocols.append(protocol.get_content())
        vserver_details = {
            'name': vserver_info.get_child_content('vserver-name'),
            'aggr_list': aggr_list,
            'allowed_protocols': protocols,
        }
    return vserver_details