def rename_aggregate(self):
    '\n        rename aggregate.\n        '
    aggr_rename = netapp_utils.zapi.NaElement.create_node_with_children('aggr-rename', **{
        'aggregate': self.name,
        'new-aggregate-name': self.rename,
    })
    try:
        self.server.invoke_successfully(aggr_rename, enable_tunneling=False)
    except netapp_utils.zapi.NaApiError as error:
        self.module.fail_json(msg=('Error renaming aggregate %s: %s' % (self.name, to_native(error))), exception=traceback.format_exc())