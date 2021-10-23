def create_aggr(self):
    '\n        Create aggregate\n        :return: None\n        '
    if (not self.parameters.get('disk_count')):
        self.module.fail_json(msg=('Error provisioning aggregate %s:                                              disk_count is required' % self.parameters['name']))
    options = {
        'aggregate': self.parameters['name'],
        'disk-count': str(self.parameters['disk_count']),
    }
    if self.parameters.get('disk_type'):
        options['disk-type'] = self.parameters['disk_type']
    if self.parameters.get('raid_size'):
        options['raid-size'] = str(self.parameters['raid_size'])
    if self.parameters.get('raid_type'):
        options['raid-type'] = self.parameters['raid_type']
    if self.parameters.get('disk_size'):
        options['disk-size'] = str(self.parameters['disk_size'])
    aggr_create = netapp_utils.zapi.NaElement.create_node_with_children('aggr-create', **options)
    if self.parameters.get('nodes'):
        nodes_obj = netapp_utils.zapi.NaElement('nodes')
        aggr_create.add_child_elem(nodes_obj)
        for node in self.parameters['nodes']:
            nodes_obj.add_new_child('node-name', node)
    try:
        self.server.invoke_successfully(aggr_create, enable_tunneling=False)
    except netapp_utils.zapi.NaApiError as error:
        self.module.fail_json(msg=('Error provisioning aggregate %s: %s' % (self.parameters['name'], to_native(error))), exception=traceback.format_exc())