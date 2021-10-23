def jaccard(vec1, vec2):
    'Calculate Jaccard distance between vectors.\n\n    Parameters\n    ----------\n    vec1 : {scipy.sparse, numpy.ndarray, list of (int, float)}\n        Distribution vector.\n    vec2 : {scipy.sparse, numpy.ndarray, list of (int, float)}\n        Distribution vector.\n\n    Returns\n    -------\n    float\n        Jaccard distance between `vec1` and `vec2`.\n        Value in range [0, 1], where 0 is min distance (max similarity) and 1 is max distance (min similarity).\n\n    '
    if scipy.sparse.issparse(vec1):
        vec1 = vec1.toarray()
    if scipy.sparse.issparse(vec2):
        vec2 = vec2.toarray()
    if (isbow(vec1) and isbow(vec2)):
        union = (sum((weight for (id_, weight) in vec1)) + sum((weight for (id_, weight) in vec2)))
        (vec1, vec2) = (dict(vec1), dict(vec2))
        intersection = 0.0
        for (feature_id, feature_weight) in iteritems(vec1):
            intersection += min(feature_weight, vec2.get(feature_id, 0.0))
        return (1 - (float(intersection) / float(union)))
    else:
        if isinstance(vec1, np.ndarray):
            vec1 = vec1.tolist()
        if isinstance(vec2, np.ndarray):
            vec2 = vec2.tolist()
        vec1 = set(vec1)
        vec2 = set(vec2)
        intersection = (vec1 & vec2)
        union = (vec1 | vec2)
        return (1 - (float(len(intersection)) / float(len(union))))