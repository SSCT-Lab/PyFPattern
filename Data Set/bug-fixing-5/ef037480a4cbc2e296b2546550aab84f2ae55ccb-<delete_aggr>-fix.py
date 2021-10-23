def delete_aggr(self):
    '\n        Delete aggregate.\n        :return: None\n        '
    aggr_destroy = netapp_utils.zapi.NaElement.create_node_with_children('aggr-destroy', **{
        'aggregate': self.parameters['name'],
    })
    try:
        self.server.invoke_successfully(aggr_destroy, enable_tunneling=False)
    except netapp_utils.zapi.NaApiError as error:
        self.module.fail_json(msg=('Error removing aggregate %s: %s' % (self.parameters['name'], to_native(error))), exception=traceback.format_exc())