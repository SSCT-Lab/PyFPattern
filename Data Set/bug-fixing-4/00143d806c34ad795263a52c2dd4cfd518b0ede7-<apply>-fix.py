def apply(self):
    '\n        Check to see which play we should run\n        '
    changed = False
    comment_changed = False
    netapp_utils.ems_log_event('na_ontap_snapshot', self.server)
    existing_snapshot = self.does_snapshot_exist()
    if (existing_snapshot is not None):
        if (self.state == 'absent'):
            changed = True
        elif ((self.state == 'present') and (self.comment is not None)):
            if (existing_snapshot['comment'] != self.comment):
                comment_changed = True
                changed = True
    elif (self.state == 'present'):
        changed = True
    if changed:
        if self.module.check_mode:
            pass
        elif (self.state == 'present'):
            if (not existing_snapshot):
                self.create_snapshot()
            elif comment_changed:
                self.modify_snapshot()
        elif (self.state == 'absent'):
            if existing_snapshot:
                self.delete_snapshot()
    self.module.exit_json(changed=changed)