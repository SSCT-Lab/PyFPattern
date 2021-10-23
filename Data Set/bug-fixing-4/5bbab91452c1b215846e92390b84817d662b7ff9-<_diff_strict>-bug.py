def _diff_strict(self, other):
    updates = list()
    for (index, line) in enumerate(self._items):
        try:
            if (line != other._lines[index]):
                updates.append(line)
        except IndexError:
            updates.append(line)
    return updates