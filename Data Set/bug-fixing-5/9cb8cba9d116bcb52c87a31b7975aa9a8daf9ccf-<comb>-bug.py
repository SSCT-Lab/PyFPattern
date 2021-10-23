def comb(N, k, exact=False, repetition=False):
    'The number of combinations of N things taken k at a time.\n\n    This is often expressed as "N choose k".\n\n    Parameters\n    ----------\n    N : int, ndarray\n        Number of things.\n    k : int, ndarray\n        Number of elements taken.\n    exact : bool, optional\n        If `exact` is False, then floating point precision is used, otherwise\n        exact long integer is computed.\n    repetition : bool, optional\n        If `repetition` is True, then the number of combinations with\n        repetition is computed.\n\n    Returns\n    -------\n    val : int, ndarray\n        The total number of combinations.\n\n    See Also\n    --------\n    binom : Binomial coefficient ufunc\n\n    Notes\n    -----\n    - Array arguments accepted only for exact=False case.\n    - If k > N, N < 0, or k < 0, then a 0 is returned.\n\n    Examples\n    --------\n    >>> from scipy.special import comb\n    >>> k = np.array([3, 4])\n    >>> n = np.array([10, 10])\n    >>> comb(n, k, exact=False)\n    array([ 120.,  210.])\n    >>> comb(10, 3, exact=True)\n    120L\n    >>> comb(10, 3, exact=True, repetition=True)\n    220L\n\n    '
    if repetition:
        return comb(((N + k) - 1), k, exact)
    if exact:
        return _comb_int(N, k)
    else:
        (k, N) = (asarray(k), asarray(N))
        cond = (((k <= N) & (N >= 0)) & (k >= 0))
        vals = binom(N, k)
        if isinstance(vals, np.ndarray):
            vals[(~ cond)] = 0
        elif (not cond):
            vals = np.float64(0)
        return vals