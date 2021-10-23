def _layout_random(self):
    super_add = super(ActionView, self).add_widget
    self._state = 'random'
    self._clear_all()
    hidden_items = []
    hidden_groups = []
    total_width = 0
    super_add(self.action_previous)
    width = ((self.width - self.overflow_group.pack_width) - self.action_previous.pack_width)
    if len(self._list_action_items):
        for child in self._list_action_items[1:]:
            if child.important:
                if ((child.pack_width + total_width) < width):
                    super_add(child)
                    child.inside_group = False
                    total_width += child.pack_width
                else:
                    hidden_items.append(child)
            else:
                hidden_items.append(child)
    if (total_width < self.width):
        for group in self._list_action_group:
            if (((group.pack_width + total_width) + group.separator_width) < width):
                super_add(group)
                group.show_group()
                total_width += (group.pack_width + group.separator_width)
            else:
                hidden_groups.append(group)
    group_index = (len(self.children) - 1)
    if (total_width < self.width):
        for child in hidden_items[:]:
            if ((child.pack_width + total_width) < width):
                super_add(child, group_index)
                total_width += child.pack_width
                child.inside_group = False
                hidden_items.remove(child)
    extend_hidden = hidden_items.extend
    for group in hidden_groups:
        extend_hidden(group.list_action_item)
    overflow_group = self.overflow_group
    if (hidden_items != []):
        over_add = super(overflow_group.__class__, overflow_group).add_widget
        for child in hidden_items:
            over_add(child)
        overflow_group.show_group()
        super_add(overflow_group)