def aggregate_online(self):
    '\n        enable aggregate (online).\n        '
    online_aggr = netapp_utils.zapi.NaElement.create_node_with_children('aggr-online', **{
        'aggregate': self.name,
        'force-online': 'true',
    })
    try:
        self.server.invoke_successfully(online_aggr, enable_tunneling=True)
        return True
    except netapp_utils.zapi.NaApiError as error:
        if (to_native(error.code) == '13060'):
            return False
        else:
            self.module.fail_json(msg=('Error changing the state of aggregate %s to %s: %s' % (self.name, self.service_state, to_native(error))), exception=traceback.format_exc())