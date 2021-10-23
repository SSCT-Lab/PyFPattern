def get_export_policy_rule(self):
    '\n        Return details about the export policy rule\n        :param:\n            name : Name of the export_policy\n        :return: Details about the export_policy. None if not found.\n        :rtype: dict\n        '
    rule_iter = netapp_utils.zapi.NaElement('export-rule-get-iter')
    rule_info = netapp_utils.zapi.NaElement('export-rule-info')
    rule_info.add_new_child('policy-name', self.policy_name)
    if self.vserver:
        rule_info.add_new_child('vserver-name', self.vserver)
    if self.client_match:
        rule_info.add_new_child('client-match', self.client_match)
    query = netapp_utils.zapi.NaElement('query')
    query.add_child_elem(rule_info)
    rule_iter.add_child_elem(query)
    result = self.server.invoke_successfully(rule_iter, True)
    return_value = None
    if (result.get_child_by_name('num-records') and (int(result.get_child_content('num-records')) == 1)):
        export_policy_rule_details = result.get_child_by_name('attributes-list').get_child_by_name('export-rule-info')
        export_policy_name = export_policy_rule_details.get_child_content('policy-name')
        export_rule_index = export_policy_rule_details.get_child_content('rule-index')
        export_rule_protocol = export_policy_rule_details.get_child_by_name('protocol').get_child_content('access-protocol')
        export_rule_ro_rule = export_policy_rule_details.get_child_by_name('ro-rule').get_child_content('security-flavor')
        export_rule_rw_rule = export_policy_rule_details.get_child_by_name('rw-rule').get_child_content('security-flavor')
        export_rule_super_user_security = export_policy_rule_details.get_child_by_name('super-user-security').get_child_content('security-flavor')
        export_rule_allow_suid = (True if (export_policy_rule_details.get_child_content('is-allow-set-uid-enabled') == 'true') else False)
        export_rule_client_match = export_policy_rule_details.get_child_content('client-match')
        export_vserver = export_policy_rule_details.get_child_content('vserver-name')
        return_value = {
            'policy-name': export_policy_name,
            'rule-index': export_rule_index,
            'protocol': export_rule_protocol,
            'ro-rule': export_rule_ro_rule,
            'rw-rule': export_rule_rw_rule,
            'super-user-security': export_rule_super_user_security,
            'is-allow-set-uid-enabled': export_rule_allow_suid,
            'client-match': export_rule_client_match,
            'vserver': export_vserver,
        }
    elif (result.get_child_by_name('num-records') and (int(result.get_child_content('num-records')) >= 1)):
        return_value = {
            'policy-name': self.policy_name,
        }
    return return_value