

def difference(self, other, path=None, match='line', replace='line'):
    try:
        if (path and (match != 'line')):
            try:
                other = other.get_section_objects(path)
            except ValueError:
                other = list()
        else:
            other = other.items
        func = getattr(self, ('diff_%s' % match))
        updates = func(other, path=path)
    except AttributeError:
        raise
        raise TypeError('invalid value for match keyword')
    if (self._device_os == 'junos'):
        return updates
    if (replace == 'block'):
        parents = list()
        for u in updates:
            if (u.parents is None):
                if (u not in parents):
                    parents.append(u)
            else:
                for p in u.parents:
                    if (p not in parents):
                        parents.append(p)
        return self.expand_block(parents)
    return self.expand_line(updates)
