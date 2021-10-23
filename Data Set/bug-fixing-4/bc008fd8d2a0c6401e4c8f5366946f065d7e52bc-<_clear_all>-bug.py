def _clear_all(self):
    self.clear_widgets()
    for group in self._list_action_group:
        group.clear_widgets()
    self.overflow_group.clear_widgets()
    self.overflow_group.list_action_item = []