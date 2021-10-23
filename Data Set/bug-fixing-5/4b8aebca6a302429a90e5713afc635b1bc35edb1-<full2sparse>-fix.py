def full2sparse(vec, eps=1e-09):
    'Convert a dense array into the BoW format.\n\n    Parameters\n    ----------\n    vec : numpy.ndarray\n        Input dense vector\n    eps : float\n        Threshold value, if coordinate in `vec` < eps, this will not be presented in result.\n\n    Returns\n    -------\n    list of (int, float)\n        BoW format of `vec`.\n\n    See Also\n    --------\n    :func:`~gensim.matutils.sparse2full`\n\n    '
    vec = np.asarray(vec, dtype=float)
    nnz = np.nonzero((abs(vec) > eps))[0]
    return list(zip(nnz, vec.take(nnz)))