def modify_vserver(self, allowed_protocols, aggr_list):
    vserver_modify = netapp_utils.zapi.NaElement.create_node_with_children('vserver-modify', **{
        'vserver-name': self.name,
    })
    if allowed_protocols:
        allowed_protocols = netapp_utils.zapi.NaElement('allowed-protocols')
        for protocol in self.allowed_protocols:
            allowed_protocols.add_new_child('protocol', protocol)
        vserver_modify.add_child_elem(allowed_protocols)
    if aggr_list:
        aggregates = netapp_utils.zapi.NaElement('aggr-list')
        for aggr in self.aggr_list:
            aggregates.add_new_child('aggr-name', aggr)
        vserver_modify.add_child_elem(aggregates)
    try:
        self.server.invoke_successfully(vserver_modify, enable_tunneling=False)
    except netapp_utils.zapi.NaApiError as e:
        self.module.fail_json(msg=('Error modifying SVM %s: %s' % (self.name, to_native(e))), exception=traceback.format_exc())