def create_export_policy_rule(self):
    '\n        create rule for the export policy.\n        '
    if (self.allow_suid is not None):
        export_rule_create = netapp_utils.zapi.NaElement.create_node_with_children('export-rule-create', **{
            'policy-name': self.policy_name,
            'client-match': self.client_match,
            'is-allow-set-uid-enabled': str(self.allow_suid),
        })
    else:
        export_rule_create = netapp_utils.zapi.NaElement.create_node_with_children('export-rule-create', **{
            'policy-name': self.policy_name,
            'client-match': self.client_match,
        })
    export_rule_create.add_node_with_children('ro-rule', **{
        'security-flavor': self.ro_rule,
    })
    export_rule_create.add_node_with_children('rw-rule', **{
        'security-flavor': self.rw_rule,
    })
    if self.protocol:
        export_rule_create.add_node_with_children('protocol', **{
            'access-protocol': self.protocol,
        })
    if self.super_user_security:
        export_rule_create.add_node_with_children('super-user-security', **{
            'security-flavor': self.super_user_security,
        })
    try:
        self.server.invoke_successfully(export_rule_create, enable_tunneling=True)
    except netapp_utils.zapi.NaApiError as error:
        self.module.fail_json(msg=('Error creating export policy rule %s: %s' % (self.policy_name, to_native(error))), exception=traceback.format_exc())