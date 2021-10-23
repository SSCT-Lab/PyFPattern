def convert_vec(vec1, vec2, num_features=None):
    '\n    Convert vectors to appropriate forms required by entropy input.\n    Checks for sparsity and bag of word format.\n    '
    if scipy.sparse.issparse(vec1):
        vec1 = vec1.toarray()
    if scipy.sparse.issparse(vec2):
        vec2 = vec2.toarray()
    if (isbow(vec1) and isbow(vec2)):
        if (num_features is not None):
            dense1 = sparse2full(vec1, num_features)
            dense2 = sparse2full(vec2, num_features)
            return (dense1, dense2)
        else:
            max_len = max(len(vec1), len(vec2))
            dense1 = sparse2full(vec1, max_len)
            dense2 = sparse2full(vec2, max_len)
            return (dense1, dense2)
    else:
        if (len(vec1) == 1):
            vec1 = vec1[0]
        if (len(vec2) == 1):
            vec2 = vec2[0]
        return (vec1, vec2)