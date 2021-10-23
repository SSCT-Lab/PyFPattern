def _layout_group(self):
    super_add = super(ActionView, self).add_widget
    self._state = 'group'
    self._clear_all()
    super_add(self.action_previous)
    if (len(self._list_action_items) > 1):
        for child in self._list_action_items[1:]:
            super_add(child)
            child.inside_group = False
    for group in self._list_action_group:
        super_add(group)
        group.show_group()
    self.overflow_group.show_default_items(self)