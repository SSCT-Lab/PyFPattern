def on_use_separator(self, instance, value):
    for group in self._list_action_group:
        group.use_separator = value
    if self.overflow_group:
        self.overflow_group.use_separator = value