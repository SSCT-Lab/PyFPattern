def _diff_exact(self, other):
    updates = list()
    if (len(other) != len(self._items)):
        updates.extend(self._items)
    else:
        for (ours, theirs) in zip(self._items, other):
            if (ours != theirs):
                updates.extend(self._items)
                break
    return updates