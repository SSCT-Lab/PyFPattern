def state_unchanged(self):
    '\n        Return unchanged state\n\n        '
    self.module.exit_json(changed=False)