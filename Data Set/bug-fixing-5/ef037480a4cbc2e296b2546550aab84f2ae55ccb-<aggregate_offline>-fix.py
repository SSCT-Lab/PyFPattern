def aggregate_offline(self):
    '\n        Set state of an online aggregate to offline\n        :return: None\n        '
    offline_aggr = netapp_utils.zapi.NaElement.create_node_with_children('aggr-offline', **{
        'aggregate': self.parameters['name'],
        'force-offline': 'false',
        'unmount-volumes': str(self.parameters['unmount_volumes']),
    })
    try:
        self.server.invoke_successfully(offline_aggr, enable_tunneling=True)
    except netapp_utils.zapi.NaApiError as error:
        self.module.fail_json(msg=('Error changing the state of aggregate %s to %s: %s' % (self.parameters['name'], self.parameters['service_state'], to_native(error))), exception=traceback.format_exc())