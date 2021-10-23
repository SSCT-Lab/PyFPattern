

def symmetric_difference(a, b):
    if (isinstance(a, collections.Hashable) and isinstance(b, collections.Hashable)):
        c = (set(a) ^ set(b))
    else:
        c = unique([x for x in union(a, b) if (x not in intersect(a, b))])
    return c
