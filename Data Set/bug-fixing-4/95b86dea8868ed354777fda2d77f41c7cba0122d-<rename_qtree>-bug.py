def rename_qtree(self):
    path = ('/vol/%s/%s' % (self.flexvol_name, self.name))
    new_path = ('/vol/%s/%s' % (self.flexvol_name, self.new_name))
    qtree_rename = netapp_utils.zapi.NaElement.create_node_with_children('qtree-rename', **{
        'qtree': path,
        'new-qtree-name': new_path,
    })
    try:
        self.server.invoke_successfully(qtree_rename, enable_tunneling=True)
    except netapp_utils.zapi.NaApiError as e:
        self.module.fail_json(msg=('Error renaming qtree %s: %s' % (self.name, to_native(e))), exception=traceback.format_exc())