def hellinger(vec1, vec2):
    'Calculate Hellinger distance between two probability distributions.\n\n    Parameters\n    ----------\n    vec1 : {scipy.sparse, numpy.ndarray, list of (int, float)}\n        Distribution vector.\n    vec2 : {scipy.sparse, numpy.ndarray, list of (int, float)}\n        Distribution vector.\n\n    Returns\n    -------\n    float\n        Hellinger distance between `vec1` and `vec2`.\n        Value in range [0, 1], where 0 is min distance (max similarity) and 1 is max distance (min similarity).\n\n    '
    if scipy.sparse.issparse(vec1):
        vec1 = vec1.toarray()
    if scipy.sparse.issparse(vec2):
        vec2 = vec2.toarray()
    if (isbow(vec1) and isbow(vec2)):
        (vec1, vec2) = (dict(vec1), dict(vec2))
        if (len(vec2) < len(vec1)):
            (vec1, vec2) = (vec2, vec1)
        sim = np.sqrt((0.5 * sum((((np.sqrt(value) - np.sqrt(vec2.get(index, 0.0))) ** 2) for (index, value) in iteritems(vec1)))))
        return sim
    else:
        sim = np.sqrt((0.5 * ((np.sqrt(vec1) - np.sqrt(vec2)) ** 2).sum()))
        return sim