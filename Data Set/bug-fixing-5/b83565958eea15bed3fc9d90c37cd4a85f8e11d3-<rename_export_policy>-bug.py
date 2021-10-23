def rename_export_policy(self):
    '\n        Rename the export-policy.\n        '
    export_policy_rename = netapp_utils.zapi.NaElement.create_node_with_children('export-policy-rename', **{
        'policy-name': self.name,
        'new-policy-name': self.new_name,
    })
    try:
        self.server.invoke_successfully(export_policy_rename, enable_tunneling=True)
    except netapp_utils.zapi.NaApiError as error:
        self.module.fail_json(msg=('Error renaming export-policy %s:%s' % (self.name, to_native(error))), exception=traceback.format_exc())