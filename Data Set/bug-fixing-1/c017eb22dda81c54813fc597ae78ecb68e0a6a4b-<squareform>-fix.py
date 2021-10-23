

def squareform(X, force='no', checks=True):
    "\n    Converts a vector-form distance vector to a square-form distance\n    matrix, and vice-versa.\n\n    Parameters\n    ----------\n    X : ndarray\n        Either a condensed or redundant distance matrix.\n    force : str, optional\n        As with MATLAB(TM), if force is equal to 'tovector' or 'tomatrix',\n        the input will be treated as a distance matrix or distance vector\n        respectively.\n    checks : bool, optional\n        If `checks` is set to False, no checks will be made for matrix\n        symmetry nor zero diagonals. This is useful if it is known that\n        ``X - X.T1`` is small and ``diag(X)`` is close to zero.\n        These values are ignored any way so they do not disrupt the\n        squareform transformation.\n\n    Returns\n    -------\n    Y : ndarray\n        If a condensed distance matrix is passed, a redundant one is\n        returned, or if a redundant one is passed, a condensed distance\n        matrix is returned.\n\n    Notes\n    -----\n\n    1. v = squareform(X)\n\n       Given a square d-by-d symmetric distance matrix X,\n       ``v=squareform(X)`` returns a ``d * (d-1) / 2`` (or\n       `${n \\choose 2}$`) sized vector v.\n\n      v[{n \\choose 2}-{n-i \\choose 2} + (j-i-1)] is the distance\n      between points i and j. If X is non-square or asymmetric, an error\n      is returned.\n\n    2. X = squareform(v)\n\n      Given a d*d(-1)/2 sized v for some integer d>=2 encoding distances\n      as described, X=squareform(v) returns a d by d distance matrix X. The\n      X[i, j] and X[j, i] values are set to\n      v[{n \\choose 2}-{n-i \\choose 2} + (j-i-1)] and all\n      diagonal elements are zero.\n\n    "
    X = _convert_to_double(np.asarray(X, order='c'))
    s = X.shape
    if (force.lower() == 'tomatrix'):
        if (len(s) != 1):
            raise ValueError("Forcing 'tomatrix' but input X is not a distance vector.")
    elif (force.lower() == 'tovector'):
        if (len(s) != 2):
            raise ValueError("Forcing 'tovector' but input X is not a distance matrix.")
    if (len(s) == 1):
        if (X.shape[0] == 0):
            return np.zeros((1, 1), dtype=np.double)
        d = int(np.ceil(np.sqrt((X.shape[0] * 2))))
        if (((d * (d - 1)) / 2) != int(s[0])):
            raise ValueError('Incompatible vector size. It must be a binomial coefficient n choose 2 for some integer n >= 2.')
        M = np.zeros((d, d), dtype=np.double)
        X = _copy_array_if_base_present(X)
        _distance_wrap.to_squareform_from_vector_wrap(M, X)
        return M
    elif (len(s) == 2):
        if (s[0] != s[1]):
            raise ValueError('The matrix argument must be square.')
        if checks:
            is_valid_dm(X, throw=True, name='X')
        d = s[0]
        if (d <= 1):
            return np.array([], dtype=np.double)
        v = np.zeros(((d * (d - 1)) // 2), dtype=np.double)
        X = _copy_array_if_base_present(X)
        _distance_wrap.to_vector_from_squareform_wrap(X, v)
        return v
    else:
        raise ValueError(('The first argument must be one or two dimensional array. A %d-dimensional array is not permitted' % len(s)))
