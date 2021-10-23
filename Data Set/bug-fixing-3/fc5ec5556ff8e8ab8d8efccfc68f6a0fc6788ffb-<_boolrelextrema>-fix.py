def _boolrelextrema(data, comparator, axis=0, order=1, mode='clip'):
    "\n    Calculate the relative extrema of `data`.\n\n    Relative extrema are calculated by finding locations where\n    ``comparator(data[n], data[n+1:n+order+1])`` is True.\n\n    Parameters\n    ----------\n    data : ndarray\n        Array in which to find the relative extrema.\n    comparator : callable\n        Function to use to compare two data points.\n        Should take two arrays as arguments.\n    axis : int, optional\n        Axis over which to select from `data`.  Default is 0.\n    order : int, optional\n        How many points on each side to use for the comparison\n        to consider ``comparator(n,n+x)`` to be True.\n    mode : str, optional\n        How the edges of the vector are treated.  'wrap' (wrap around) or\n        'clip' (treat overflow as the same as the last (or first) element).\n        Default 'clip'.  See numpy.take\n\n    Returns\n    -------\n    extrema : ndarray\n        Boolean array of the same shape as `data` that is True at an extrema,\n        False otherwise.\n\n    See also\n    --------\n    argrelmax, argrelmin\n\n    Examples\n    --------\n    >>> testdata = np.array([1,2,3,2,1])\n    >>> _boolrelextrema(testdata, np.greater, axis=0)\n    array([False, False,  True, False, False], dtype=bool)\n\n    "
    if ((int(order) != order) or (order < 1)):
        raise ValueError('Order must be an int >= 1')
    datalen = data.shape[axis]
    locs = np.arange(0, datalen)
    results = np.ones(data.shape, dtype=bool)
    main = data.take(locs, axis=axis, mode=mode)
    for shift in xrange(1, (order + 1)):
        plus = data.take((locs + shift), axis=axis, mode=mode)
        minus = data.take((locs - shift), axis=axis, mode=mode)
        results &= comparator(main, plus)
        results &= comparator(main, minus)
        if (~ results.any()):
            return results
    return results