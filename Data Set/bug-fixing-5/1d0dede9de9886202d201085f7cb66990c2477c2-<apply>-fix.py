def apply(self):
    changed = False
    igroup_exists = False
    rename_igroup = False
    initiator_changed = False
    netapp_utils.ems_log_event('na_ontap_igroup', self.server)
    igroup_details = self.get_igroup(self.name)
    if (igroup_details is not None):
        igroup_exists = True
        if (self.state == 'absent'):
            changed = True
        elif (self.state == 'present'):
            if self.initiator:
                changed = True
    elif (self.state == 'present'):
        changed = True
        if self.from_name:
            igroup_details = self.get_igroup(self.from_name)
            if (igroup_details is not None):
                rename_igroup = True
                igroup_exists = True
            else:
                self.module.fail_json(msg=('Error renaming igroup %s does not exist' % self.from_name))
    if changed:
        changed = False
        if self.module.check_mode:
            pass
        elif (self.state == 'present'):
            if (not igroup_exists):
                self.create_igroup()
                changed = True
            else:
                if self.initiator:
                    changed = self.add_initiator()
                if rename_igroup:
                    self.rename_igroup()
                    changed = True
        elif (self.state == 'absent'):
            if self.initiator:
                self.remove_initiator()
            self.delete_igroup()
            changed = True
    self.module.exit_json(changed=changed)