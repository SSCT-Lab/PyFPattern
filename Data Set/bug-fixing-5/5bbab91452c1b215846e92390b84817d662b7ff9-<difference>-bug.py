def difference(self, other, match='line', path=None, replace=None):
    try:
        meth = getattr(self, ('_diff_%s' % match))
        updates = meth(other)
    except AttributeError:
        raise TypeError('invalid value for match keyword argument, valid values are line, strict, or exact')
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