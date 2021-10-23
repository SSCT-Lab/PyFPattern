def rename_igroup(self):
    '\n        Rename the igroup.\n        '
    igroup_rename = netapp_utils.zapi.NaElement.create_node_with_children('igroup-rename', **{
        'initiator-group-name': self.from_name,
        'initiator-group-new-name': str(self.name),
    })
    try:
        self.server.invoke_successfully(igroup_rename, enable_tunneling=True)
    except netapp_utils.zapi.NaApiError as error:
        self.module.fail_json(msg=('Error renaming igroup %s: %s' % (self.name, to_native(error))), exception=traceback.format_exc())