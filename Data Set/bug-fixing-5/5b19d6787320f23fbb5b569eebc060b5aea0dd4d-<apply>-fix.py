def apply(self):
    'Apply action to export-policy'
    changed = False
    export_policy_rule_exists = None
    export_rule_protocol_changed = False
    export_rule_ro_rule_changed = False
    export_rule_rw_rule_changed = False
    export_rule_allow_suid_enabled = False
    export_rule_clientmatch_changed = False
    export_rule_superuser_changed = False
    netapp_utils.ems_log_event('na_ontap_export_policy_rules', self.server)
    export_policy_details = self.get_export_policy()
    if (not export_policy_details):
        if (self.state == 'present'):
            self.create_export_policy()
    export_policy_rule_exists = self.get_export_policy_rule()
    if (self.state == 'absent'):
        if export_policy_rule_exists:
            changed = True
            rule_index = export_policy_rule_exists['rule-index']
    elif (self.state == 'present'):
        if export_policy_rule_exists:
            rule_index = export_policy_rule_exists['rule-index']
            if rule_index:
                if ((self.protocol is not None) and (export_policy_rule_exists['protocol'] != self.protocol)):
                    export_rule_protocol_changed = True
                    changed = True
                if ((self.ro_rule is not None) and (export_policy_rule_exists['ro-rule'] != self.ro_rule)):
                    export_rule_ro_rule_changed = True
                    changed = True
                if ((self.rw_rule is not None) and (export_policy_rule_exists['rw-rule'] != self.rw_rule)):
                    export_rule_rw_rule_changed = True
                    changed = True
                if ((self.allow_suid is not None) and (export_policy_rule_exists['is-allow-set-uid-enabled'] != self.allow_suid)):
                    export_rule_allow_suid_enabled = True
                    changed = True
                if ((self.super_user_security is not None) and (export_policy_rule_exists['super-user-security'] != self.super_user_security)):
                    export_rule_superuser_changed = True
                    changed = True
                if ((self.client_match is not None) and (export_policy_rule_exists['client-match'] != self.client_match)):
                    export_rule_clientmatch_changed = True
                    changed = True
        else:
            changed = True
    if changed:
        if self.module.check_mode:
            pass
        elif (self.state == 'present'):
            if (not export_policy_rule_exists):
                self.create_export_policy_rule()
            else:
                if export_rule_protocol_changed:
                    self.modify_protocol(rule_index)
                if export_rule_ro_rule_changed:
                    self.modify_ro_rule(rule_index)
                if export_rule_rw_rule_changed:
                    self.modify_rw_rule(rule_index)
                if export_rule_allow_suid_enabled:
                    self.modify_allow_suid(rule_index)
                if export_rule_clientmatch_changed:
                    self.modify_client_match(rule_index)
                if export_rule_superuser_changed:
                    self.modify_super_user_security(rule_index)
        elif (self.state == 'absent'):
            self.delete_export_policy_rule(rule_index)
    self.module.exit_json(changed=changed)