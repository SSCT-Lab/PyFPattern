def kullback_leibler(vec1, vec2, num_features=None):
    '\n    A distance metric between two probability distributions.\n    Returns a distance value in range <0,1> where values closer to 0 mean less distance (and a higher similarity)\n    Uses the scipy.stats.entropy method to identify kullback_leibler convergence value.\n    If the distribution draws from a certain number of docs, that value must be passed.\n    '
    if scipy.sparse.issparse(vec1):
        vec1 = vec1.toarray()
    if scipy.sparse.issparse(vec2):
        vec2 = vec2.toarray()
    if (isbow(vec1) and isbow(vec2)):
        if (num_features is not None):
            dense1 = sparse2full(vec1, num_features)
            dense2 = sparse2full(vec2, num_features)
            return entropy(dense1, dense2)
        else:
            max_len = max(len(vec1), len(vec2))
            dense1 = sparse2full(vec1, max_len)
            dense2 = sparse2full(vec2, max_len)
            return entropy(dense1, dense2)
    else:
        if (len(vec1) == 1):
            vec1 = vec1[0]
        if (len(vec2) == 1):
            vec2 = vec2[0]
        return scipy.stats.entropy(vec1, vec2)