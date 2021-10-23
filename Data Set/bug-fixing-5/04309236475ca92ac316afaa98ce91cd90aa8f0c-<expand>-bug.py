def expand(self, obj, items):
    block = [item.raw for item in obj.parents]
    block.append(obj.raw)
    current_level = items
    for b in block:
        if (b not in current_level):
            current_level[b] = collections.OrderedDict()
        current_level = current_level[b]
    for c in obj.children:
        if (c.raw not in current_level):
            current_level[c.raw] = collections.OrderedDict()