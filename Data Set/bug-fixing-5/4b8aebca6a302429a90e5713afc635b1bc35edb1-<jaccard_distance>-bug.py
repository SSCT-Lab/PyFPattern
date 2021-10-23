def jaccard_distance(set1, set2):
    '\n    Calculate a distance between set representation (1 minus the intersection divided by union).\n    Return a value in range <0, 1> where values closer to 0 mean smaller distance and thus higher similarity.\n    '
    union_cardinality = len((set1 | set2))
    if (union_cardinality == 0):
        return 1.0
    return (1.0 - (float(len((set1 & set2))) / float(union_cardinality)))