def jaccard_distance(set1, set2):
    'Calculate Jaccard distance between two sets\n\n    Parameters\n    ----------\n    set1 : set\n        Input set.\n    set2 : set\n        Input set.\n\n    Returns\n    -------\n    float\n        Jaccard distance between `set1` and `set2`.\n        Value in range [0, 1], where 0 is min distance (max similarity) and 1 is max distance (min similarity).\n    '
    union_cardinality = len((set1 | set2))
    if (union_cardinality == 0):
        return 1.0
    return (1.0 - (float(len((set1 & set2))) / float(union_cardinality)))