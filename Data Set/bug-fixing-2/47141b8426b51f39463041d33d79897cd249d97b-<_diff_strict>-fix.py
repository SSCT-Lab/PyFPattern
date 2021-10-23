

def _diff_strict(self, other):
    updates = list()
    for (index, line) in enumerate(self.items):
        try:
            if (str(line).strip() != str(other[index]).strip()):
                updates.append(line)
        except (AttributeError, IndexError):
            updates.append(line)
    return updates
