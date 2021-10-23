def apply(self):
    '\n        Apply action to export-policy\n        '
    changed = False
    export_policy_exists = False
    netapp_utils.ems_log_event('na_ontap_export_policy', self.server)
    rename_flag = False
    export_policy_details = self.get_export_policy()
    if export_policy_details:
        export_policy_exists = True
        if (self.state == 'absent'):
            changed = True
    elif (self.state == 'present'):
        if (self.from_name is not None):
            if self.get_export_policy(self.from_name):
                changed = True
                rename_flag = True
            else:
                self.module.fail_json(msg=('Error renaming export-policy %s: does not exists' % self.from_name))
        else:
            changed = True
    if changed:
        if self.module.check_mode:
            pass
        elif (self.state == 'present'):
            if rename_flag:
                self.rename_export_policy()
            else:
                self.create_export_policy()
        elif (self.state == 'absent'):
            self.delete_export_policy()
    self.module.exit_json(changed=changed)