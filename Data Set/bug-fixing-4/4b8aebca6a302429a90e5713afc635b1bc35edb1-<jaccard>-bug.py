def jaccard(vec1, vec2):
    '\n    A distance metric between bags of words representation.\n    Returns 1 minus the intersection divided by union, where union is the sum of the size of the two bags.\n    If it is not a bag of words representation, the union and intersection is calculated in the traditional manner.\n    Returns a value in range <0,1> where values closer to 0 mean less distance and thus higher similarity.\n\n    '
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