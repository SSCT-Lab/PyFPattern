def any2sparse(vec, eps=1e-09):
    'Convert a numpy.ndarray or `scipy.sparse` vector into gensim BoW format.\n\n    Parameters\n    ----------\n    vec : {`numpy.ndarray`, `scipy.sparse`}\n        Input vector\n    eps : float, optional\n        Value used for threshold, all coordinates less than `eps` will not be presented in result.\n\n    Returns\n    -------\n    list of (int, float)\n        Vector in BoW format.\n\n    '
    if isinstance(vec, np.ndarray):
        return dense2vec(vec, eps)
    if scipy.sparse.issparse(vec):
        return scipy2sparse(vec, eps)
    return [(int(fid), float(fw)) for (fid, fw) in vec if (np.abs(fw) > eps)]