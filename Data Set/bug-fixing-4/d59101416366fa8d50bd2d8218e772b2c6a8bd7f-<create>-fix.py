def create(self):
    self._set_changed_options()
    self.set_reasonable_creation_defaults()
    if ((self.want.status == 'scheduled') and (self.want.schedule is None)):
        raise F5ModuleError("A 'schedule' must be specified when 'status' is 'scheduled'.")
    if self.module.check_mode:
        return True
    self.create_on_device()
    return True