def rename_vserver(self):
    vserver_rename = netapp_utils.zapi.NaElement.create_node_with_children('vserver-rename', **{
        'vserver-name': self.from_name,
        'new-name': self.name,
    })
    try:
        self.server.invoke_successfully(vserver_rename, enable_tunneling=False)
    except netapp_utils.zapi.NaApiError as e:
        self.module.fail_json(msg=('Error renaming SVM %s: %s' % (self.name, to_native(e))), exception=traceback.format_exc())