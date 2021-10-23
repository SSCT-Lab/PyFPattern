def remove(self):
    if self.module.check_mode:
        return True
    self.remove_from_device()
    if self.exists():
        raise F5ModuleError('Failed to remove the trusted peer.')
    return True