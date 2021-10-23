def diff_commands(commands, config):
    config = [unicode(c).replace("'", '') for c in config]
    updates = list()
    visited = set()
    for (index, item) in enumerate(commands):
        if (len(item) > 0):
            if ((not item.startswith('set')) and (not item.startswith('delete'))):
                raise ValueError('line must start with either `set` or `delete`')
            elif (item.startswith('set') and (item[4:] not in config)):
                updates.append(item)
            elif item.startswith('delete'):
                for entry in (config + commands[0:index]):
                    if entry.startswith('set'):
                        entry = entry[4:]
                    if (entry.startswith(item[7:]) and (item not in visited)):
                        updates.append(item)
                        visited.add(item)
    return updates