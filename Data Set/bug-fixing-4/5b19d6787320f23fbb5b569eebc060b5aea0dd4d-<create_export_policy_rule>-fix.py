def create_export_policy_rule(self):
    '\n        create rule for the export policy.\n        '
    options = {
        'policy-name': self.policy_name,
        'client-match': self.client_match,
    }
    if (self.allow_suid is not None):
        options['is-allow-set-uid-enabled'] = ('true' if self.allow_suid else 'false')
    if (self.rule_index is not None):
        options['rule-index'] = str(self.rule_index)
    export_rule_create = netapp_utils.zapi.NaElement.create_node_with_children('export-rule-create', **options)
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