def difference(self, other, path=None, match='line', replace='line'):
    updates = list()
    config = self.items
    if path:
        config = (self.get_children(path) or list())
    if (match == 'line'):
        for item in config:
            if (item not in other.items):
                updates.append(item)
    elif (match == 'strict'):
        if path:
            current = (other.get_children(path) or list())
        else:
            current = other.items
        for (index, item) in enumerate(config):
            try:
                if (item != current[index]):
                    updates.append(item)
            except IndexError:
                updates.append(item)
    elif (match == 'exact'):
        if path:
            current = (other.get_children(path) or list())
        else:
            current = other.items
        if (len(current) != len(config)):
            updates.extend(config)
        else:
            for (ours, theirs) in itertools.izip(config, current):
                if (ours != theirs):
                    updates.extend(config)
                    break
    if (self._device_os == 'junos'):
        return updates
    diffs = collections.OrderedDict()
    for update in updates:
        if ((replace == 'block') and update.parents):
            update = update.parents[(- 1)]
        self.expand(update, diffs)
    return self.flatten(diffs)