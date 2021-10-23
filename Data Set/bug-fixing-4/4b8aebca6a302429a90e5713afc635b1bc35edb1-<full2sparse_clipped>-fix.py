def full2sparse_clipped(vec, topn, eps=1e-09):
    'Like :func:`~gensim.matutils.full2sparse`, but only return the `topn` elements of the greatest magnitude (abs).\n\n    Parameters\n    ----------\n    vec : numpy.ndarray\n        Input dense vector\n    topn : int\n        Number of greatest (abs) elements that will be presented in result.\n    eps : float\n        Threshold value, if coordinate in `vec` < eps, this will not be presented in result.\n\n    Returns\n    -------\n    list of (int, float)\n        Clipped vector in BoW format.\n\n    See Also\n    --------\n    :func:`~gensim.matutils.full2sparse`\n\n    '
    if (topn <= 0):
        return []
    vec = np.asarray(vec, dtype=float)
    nnz = np.nonzero((abs(vec) > eps))[0]
    biggest = nnz.take(argsort(abs(vec).take(nnz), topn, reverse=True))
    return list(zip(biggest, vec.take(biggest)))