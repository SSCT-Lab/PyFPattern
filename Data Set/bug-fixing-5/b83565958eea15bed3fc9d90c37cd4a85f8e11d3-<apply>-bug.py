def apply(self):
    '\n        Apply action to export-policy\n        '
    changed = False
    export_policy_exists = False
    netapp_utils.ems_log_event('na_ontap_export_policy', self.server)
    rename_flag = False
    export_policy_details = self.get_export_policy()
    if export_policy_details:
        export_policy_exists = True
        if (self.state == 'present'):
            if (self.new_name is not None):
                if ((self.new_name != self.name) and (self.new_name != export_policy_details['policy-name'])):
                    changed = True
                    rename_flag = True
        elif (self.state == 'absent'):
            changed = True
    elif (self.state == 'present'):
        changed = True
    if changed:
        if self.module.check_mode:
            pass
        elif (self.state == 'present'):
            if (not export_policy_exists):
                self.create_export_policy()
            elif rename_flag:
                self.rename_export_policy()
        elif (self.state == 'absent'):
            self.delete_export_policy()
    self.module.exit_json(changed=changed)