def state_exit_unchanged(self):
    '\n        Declare exit without unchanged\n        '
    self.module.exit_json(changed=False)