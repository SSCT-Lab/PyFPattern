def hellinger(vec1, vec2):
    '\n    Hellinger distance is a distance metric to quantify the similarity between two probability distributions.\n    Distance between distributions will be a number between <0,1>, where 0 is minimum distance (maximum similarity)\n    and 1 is maximum distance (minimum similarity).\n    '
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