def difference(self, other, match='line', path=None, replace=None):
    "Perform a config diff against the another network config\n\n        :param other: instance of NetworkConfig to diff against\n        :param match: type of diff to perform.  valid values are 'line',\n            'strict', 'exact'\n        :param path: context in the network config to filter the diff\n        :param replace: the method used to generate the replacement lines.\n            valid values are 'block', 'line'\n\n        :returns: a string of lines that are different\n        "
    if (path and (match != 'line')):
        try:
            other = other.get_block(path)
        except ValueError:
            other = list()
    else:
        other = other.items
    meth = getattr(self, ('_diff_%s' % match))
    updates = meth(other)
    if (replace == 'block'):
        parents = list()
        for item in updates:
            if (not item.has_parents):
                parents.append(item)
            else:
                for p in item._parents:
                    if (p not in parents):
                        parents.append(p)
        updates = list()
        for item in parents:
            updates.extend(self._expand_block(item))
    visited = set()
    expanded = list()
    for item in updates:
        for p in item._parents:
            if (p.line not in visited):
                visited.add(p.line)
                expanded.append(p)
        expanded.append(item)
        visited.add(item.line)
    return expanded