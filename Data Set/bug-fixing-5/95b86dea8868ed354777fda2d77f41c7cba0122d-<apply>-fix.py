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
    elif (self.state == 'present'):
        if self.from_name:
            if (self.get_qtree(self.from_name) is None):
                self.module.fail_json(msg=('Error renaming qtree %s: does not exists' % self.from_name))
            else:
                changed = True
                rename_qtree = True
        else:
            changed = True
    if changed:
        if self.module.check_mode:
            pass
        elif (self.state == 'present'):
            if rename_qtree:
                self.rename_qtree()
            else:
                self.create_qtree()
        elif (self.state == 'absent'):
            self.delete_qtree()
    self.module.exit_json(changed=changed)