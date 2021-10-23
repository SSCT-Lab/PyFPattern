def state_unchanged(self):
    '\n        Function to return unchanged state\n\n        '
    self.module.exit_json(changed=False)