def scipy2sparse(vec, eps=1e-09):
    'Convert a scipy.sparse vector BoW format.\n\n    Parameters\n    ----------\n    vec : `scipy.sparse`\n        Sparse vector\n\n    eps : float, optional\n        Value used for threshold, all coordinates less than `eps` will not be presented in result.\n\n    Returns\n    -------\n    list of (int, float)\n        Vector in BoW format.\n\n    '
    vec = vec.tocsr()
    assert (vec.shape[0] == 1)
    return [(int(pos), float(val)) for (pos, val) in zip(vec.indices, vec.data) if (np.abs(val) > eps)]