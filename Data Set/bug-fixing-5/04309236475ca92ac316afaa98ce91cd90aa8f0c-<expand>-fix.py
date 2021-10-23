def expand(self, objs):
    visited = set()
    expanded = list()
    for o in objs:
        for p in o.parents:
            if (p not in visited):
                visited.add(p)
                expanded.append(p)
        expanded.append(o)
        visited.add(o)
    return expanded