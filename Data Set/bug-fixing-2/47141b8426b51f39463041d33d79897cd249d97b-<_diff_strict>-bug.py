

def _diff_strict(self, other):
    updates = list()
    for (index, line) in enumerate(self.items):
        try:
            if (line != other[index]):
                updates.append(line)
        except IndexError:
            updates.append(line)
    return updates
