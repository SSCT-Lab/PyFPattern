

def diff_commands(commands, config):
    config = [unicode(c).replace("'", '') for c in config]
    updates = list()
    visited = set()
    for item in commands:
        if (len(item) > 0):
            if ((not item.startswith('set')) and (not item.startswith('delete'))):
                raise ValueError('line must start with either `set` or `delete`')
            elif (item.startswith('set') and (item[4:] not in config)):
                updates.append(item)
            elif item.startswith('delete'):
                for entry in config:
                    if (entry.startswith(item[7:]) and (item not in visited)):
                        updates.append(item)
                        visited.add(item)
    return updates
