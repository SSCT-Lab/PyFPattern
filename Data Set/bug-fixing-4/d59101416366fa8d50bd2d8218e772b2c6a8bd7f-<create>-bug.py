def create(self):
    self._set_changed_options()
    if ((self.want.rule_list is None) and (self.want.parent_rule_list is None)):
        if (self.want.action is None):
            self.changes.update({
                'action': 'reject',
            })
        if (self.want.logging is None):
            self.changes.update({
                'logging': False,
            })
    if (self.want.status is None):
        self.changes.update({
            'status': 'enabled',
        })
    if ((self.want.status == 'scheduled') and (self.want.schedule is None)):
        raise F5ModuleError("A 'schedule' must be specified when 'status' is 'scheduled'.")
    if self.module.check_mode:
        return True
    self.create_on_device()
    return True