def apply(self):
    exists = self.get_fcp()
    changed = False
    if (self.parameters['state'] == 'present'):
        if exists:
            if (self.parameters['status'] == 'up'):
                if (not self.current_status()):
                    self.start_fcp()
                    changed = True
            elif self.current_status():
                self.stop_fcp()
                changed = True
        else:
            self.create_fcp()
            if (self.parameters['status'] == 'up'):
                self.start_fcp()
            changed = True
    elif exists:
        if self.current_status():
            self.stop_fcp()
        self.destroy_fcp()
        changed = True
    self.module.exit_json(changed=changed)