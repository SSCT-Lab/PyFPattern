def aggregate_offline(self):
    '\n        disable aggregate (offline).\n        '
    offline_aggr = netapp_utils.zapi.NaElement.create_node_with_children('aggr-offline', **{
        'aggregate': self.name,
        'force-offline': 'false',
        'unmount-volumes': str(self.unmount_volumes),
    })
    try:
        self.server.invoke_successfully(offline_aggr, enable_tunneling=True)
        return True
    except netapp_utils.zapi.NaApiError as error:
        if (to_native(error.code) == '13042'):
            return False
        else:
            self.module.fail_json(msg=('Error changing the state of aggregate %s to %s: %s' % (self.name, self.service_state, to_native(error))), exception=traceback.format_exc())