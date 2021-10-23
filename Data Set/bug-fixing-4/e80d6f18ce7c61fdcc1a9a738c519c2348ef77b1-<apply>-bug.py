def apply(self):
    ' Apply required action from the play'
    self.autosupport_log()
    if (self.parameters.get('client_match') is not None):
        self.parameters['client_match'] = ','.join(self.parameters['client_match'])
    (current, modify) = (self.get_export_policy_rule(), None)
    action = self.na_helper.get_cd_action(current, self.parameters)
    if ((action is None) and (self.parameters['state'] == 'present')):
        modify = self.na_helper.get_modified_attributes(current, self.parameters)
    if self.na_helper.changed:
        if self.module.check_mode:
            pass
        else:
            if (not self.get_export_policy()):
                self.create_export_policy()
            if (action == 'create'):
                self.create_export_policy_rule()
            elif (action == 'delete'):
                if (current['num_records'] > 1):
                    self.module.fail_json(msg='Multiple export policy rules exist.Please specify a rule_index to delete')
                self.delete_export_policy_rule(current['rule_index'])
            elif modify:
                self.modify_export_policy_rule(modify)
    self.module.exit_json(changed=self.na_helper.changed)