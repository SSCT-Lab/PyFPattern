def apply(self):
    changed = False
    vserver = netapp_utils.setup_na_ontap_zapi(module=self.module, vserver=self.vserver)
    netapp_utils.ems_log_event('na_ontap_user_role', vserver)
    role_exists = self.get_role()
    if role_exists:
        if (self.state == 'absent'):
            changed = True
    elif (self.state == 'present'):
        changed = True
    if changed:
        if self.module.check_mode:
            pass
        elif (self.state == 'present'):
            if (not role_exists):
                self.create_role()
        elif (self.state == 'absent'):
            self.delete_role()
    self.module.exit_json(changed=changed)