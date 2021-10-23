

def deselect_node(self, *args):
    'Deselect any selected node.\n\n        .. versionadded:: 1.10.0\n        '
    if self._selected_node:
        self._selected_node.is_selected = False
