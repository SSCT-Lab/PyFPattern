def delete_export_policy_rule(self, rule_index):
    '\n        delete rule for the export policy.\n        '
    export_rule_delete = netapp_utils.zapi.NaElement.create_node_with_children('export-rule-destroy', **{
        'policy-name': self.parameters['name'],
        'rule-index': str(rule_index),
    })
    try:
        self.server.invoke_successfully(export_rule_delete, enable_tunneling=True)
    except netapp_utils.zapi.NaApiError as error:
        self.module.fail_json(msg=('Error deleting export policy rule %s: %s' % (self.parameters['name'], to_native(error))), exception=traceback.format_exc())