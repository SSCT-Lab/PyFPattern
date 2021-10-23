def apply(self):
    changed = False
    qtree_exists = False
    rename_qtree = False
    netapp_utils.ems_log_event('na_ontap_qtree', self.server)
    qtree_detail = self.get_qtree()
    if qtree_detail:
        qtree_exists = True
        if (self.state == 'absent'):
            changed = True
        elif (self.new_name and (self.name != self.new_name)):
            changed = True
            rename_qtree = True
    elif (self.state == 'present'):
        changed = True
    if changed:
        if self.module.check_mode:
            pass
        elif (self.state == 'present'):
            if (not qtree_exists):
                self.create_qtree()
            elif rename_qtree:
                self.rename_qtree()
        elif (self.state == 'absent'):
            self.delete_qtree()
    self.module.exit_json(changed=changed)