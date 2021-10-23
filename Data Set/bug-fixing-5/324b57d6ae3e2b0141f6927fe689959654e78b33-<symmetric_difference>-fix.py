def symmetric_difference(a, b):
    if (isinstance(a, collections.Hashable) and isinstance(b, collections.Hashable)):
        c = (set(a) ^ set(b))
    else:
        isect = intersect(a, b)
        c = [x for x in union(a, b) if (x not in isect)]
    return c