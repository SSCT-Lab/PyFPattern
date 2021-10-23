def aggregate_online(self):
    '\n        Set state of an offline aggregate to online\n        :return: None\n        '
    online_aggr = netapp_utils.zapi.NaElement.create_node_with_children('aggr-online', **{
        'aggregate': self.parameters['name'],
        'force-online': 'true',
    })
    try:
        self.server.invoke_successfully(online_aggr, enable_tunneling=True)
    except netapp_utils.zapi.NaApiError as error:
        self.module.fail_json(msg=('Error changing the state of aggregate %s to %s: %s' % (self.parameters['name'], self.parameters['service_state'], to_native(error))), exception=traceback.format_exc())