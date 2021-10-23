def modify_allow_suid(self, rule_index):
    '\n        Modify allow_suid.\n        '
    export_rule_modify_allow_suid = netapp_utils.zapi.NaElement.create_node_with_children('export-rule-modify', **{
        'policy-name': self.policy_name,
        'rule-index': rule_index,
        'is-allow-set-uid-enabled': str(self.allow_suid),
    })
    try:
        self.server.invoke_successfully(export_rule_modify_allow_suid, enable_tunneling=True)
    except netapp_utils.zapi.NaApiError as error:
        self.module.fail_json(msg=('Error modifying allow_suid %s: %s' % (self.allow_suid, to_native(error))), exception=traceback.format_exc())