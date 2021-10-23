def state_exit_unchanged(self):
    '\n        Function to declare exit without unchanged\n        '
    self.module.exit_json(changed=False)