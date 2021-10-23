def _layout_all(self):
    super_add = super(ActionView, self).add_widget
    self._state = 'all'
    self._clear_all()
    super_add(self.action_previous)
    if (len(self._list_action_items) > 1):
        for child in self._list_action_items[1:]:
            child.inside_group = False
            super_add(child)
    for group in self._list_action_group:
        if (group.mode == 'spinner'):
            super_add(group)
            group.show_group()
        else:
            if (group.list_action_item != []):
                super_add(ActionSeparator())
            for child in group.list_action_item:
                child.inside_group = False
                super_add(child)
    self.overflow_group.show_default_items(self)