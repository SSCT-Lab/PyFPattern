def _diff_exact(self, other):
    updates = list()
    if (len(other) != len(self.items)):
        updates.extend(self.items)
    else:
        for (ours, theirs) in zip(self.items, other):
            if (ours != theirs):
                updates.extend(self.items)
                break
    return updates