def apply(self):
    changed = False
    igroup_exists = False
    rename_igroup = False
    initiator_changed = False
    check = False
    netapp_utils.ems_log_event('na_ontap_igroup', self.server)
    igroup_detail = self.get_igroup()
    if igroup_detail:
        igroup_exists = True
        if (self.state == 'absent'):
            changed = True
        elif (self.state == 'present'):
            if ((self.new_name is not None) and (self.new_name != self.name)):
                rename_igroup = True
                changed = True
            if changed:
                check = True
            if self.initiator:
                changed = True
    elif (self.state == 'present'):
        changed = True
    if changed:
        if self.module.check_mode:
            pass
        elif (self.state == 'present'):
            if (not igroup_exists):
                self.create_igroup()
            else:
                if self.initiator:
                    initiator_changed = self.add_initiator()
                if rename_igroup:
                    self.rename_igroup()
                if ((not check) and (not initiator_changed)):
                    changed = False
        elif (self.state == 'absent'):
            if self.initiator:
                self.remove_initiator()
            self.delete_igroup()
    self.module.exit_json(changed=changed)