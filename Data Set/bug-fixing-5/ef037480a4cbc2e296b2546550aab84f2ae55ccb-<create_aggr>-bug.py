def create_aggr(self):
    '\n        create aggregate.\n        '
    aggr_create = netapp_utils.zapi.NaElement.create_node_with_children('aggr-create', **{
        'aggregate': self.name,
        'disk-count': str(self.disk_count),
    })
    if (self.nodes is not None):
        nodes_obj = netapp_utils.zapi.NaElement('nodes')
        aggr_create.add_child_elem(nodes_obj)
        for node in self.nodes:
            nodes_obj.add_new_child('node-name', node)
    try:
        self.server.invoke_successfully(aggr_create, enable_tunneling=False)
    except netapp_utils.zapi.NaApiError as error:
        self.module.fail_json(msg=('Error provisioning aggregate %s: %s' % (self.name, to_native(error))), exception=traceback.format_exc())