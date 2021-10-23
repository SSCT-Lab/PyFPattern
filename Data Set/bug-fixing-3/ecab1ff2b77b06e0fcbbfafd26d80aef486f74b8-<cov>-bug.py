def cov(m, y=None, rowvar=True, bias=False, ddof=None, fweights=None, aweights=None):
    '\n    Estimate a covariance matrix, given data and weights.\n\n    Covariance indicates the level to which two variables vary together.\n    If we examine N-dimensional samples, :math:`X = [x_1, x_2, ... x_N]^T`,\n    then the covariance matrix element :math:`C_{ij}` is the covariance of\n    :math:`x_i` and :math:`x_j`. The element :math:`C_{ii}` is the variance\n    of :math:`x_i`.\n\n    See the notes for an outline of the algorithm.\n\n    Parameters\n    ----------\n    m : array_like\n        A 1-D or 2-D array containing multiple variables and observations.\n        Each row of `m` represents a variable, and each column a single\n        observation of all those variables. Also see `rowvar` below.\n    y : array_like, optional\n        An additional set of variables and observations. `y` has the same form\n        as that of `m`.\n    rowvar : bool, optional\n        If `rowvar` is True (default), then each row represents a\n        variable, with observations in the columns. Otherwise, the relationship\n        is transposed: each column represents a variable, while the rows\n        contain observations.\n    bias : bool, optional\n        Default normalization (False) is by ``(N - 1)``, where ``N`` is the\n        number of observations given (unbiased estimate). If `bias` is True,\n        then normalization is by ``N``. These values can be overridden by using\n        the keyword ``ddof`` in numpy versions >= 1.5.\n    ddof : int, optional\n        If not ``None`` the default value implied by `bias` is overridden.\n        Note that ``ddof=1`` will return the unbiased estimate, even if both\n        `fweights` and `aweights` are specified, and ``ddof=0`` will return\n        the simple average. See the notes for the details. The default value\n        is ``None``.\n\n        .. versionadded:: 1.5\n    fweights : array_like, int, optional\n        1-D array of integer freguency weights; the number of times each\n        observation vector should be repeated.\n\n        .. versionadded:: 1.10\n    aweights : array_like, optional\n        1-D array of observation vector weights. These relative weights are\n        typically large for observations considered "important" and smaller for\n        observations considered less "important". If ``ddof=0`` the array of\n        weights can be used to assign probabilities to observation vectors.\n\n        .. versionadded:: 1.10\n\n    Returns\n    -------\n    out : ndarray\n        The covariance matrix of the variables.\n\n    See Also\n    --------\n    corrcoef : Normalized covariance matrix\n\n    Notes\n    -----\n    Assume that the observations are in the columns of the observation\n    array `m` and let ``f = fweights`` and ``a = aweights`` for brevity. The\n    steps to compute the weighted covariance are as follows::\n\n        >>> w = f * a\n        >>> v1 = np.sum(w)\n        >>> v2 = np.sum(w * a)\n        >>> m -= np.sum(m * w, axis=1, keepdims=True) / v1\n        >>> cov = np.dot(m * w, m.T) * v1 / (v1**2 - ddof * v2)\n\n    Note that when ``a == 1``, the normalization factor\n    ``v1 / (v1**2 - ddof * v2)`` goes over to ``1 / (np.sum(f) - ddof)``\n    as it should.\n\n    Examples\n    --------\n    Consider two variables, :math:`x_0` and :math:`x_1`, which\n    correlate perfectly, but in opposite directions:\n\n    >>> x = np.array([[0, 2], [1, 1], [2, 0]]).T\n    >>> x\n    array([[0, 1, 2],\n           [2, 1, 0]])\n\n    Note how :math:`x_0` increases while :math:`x_1` decreases. The covariance\n    matrix shows this clearly:\n\n    >>> np.cov(x)\n    array([[ 1., -1.],\n           [-1.,  1.]])\n\n    Note that element :math:`C_{0,1}`, which shows the correlation between\n    :math:`x_0` and :math:`x_1`, is negative.\n\n    Further, note how `x` and `y` are combined:\n\n    >>> x = [-2.1, -1,  4.3]\n    >>> y = [3,  1.1,  0.12]\n    >>> X = np.vstack((x,y))\n    >>> print(np.cov(X))\n    [[ 11.71        -4.286     ]\n     [ -4.286        2.14413333]]\n    >>> print(np.cov(x, y))\n    [[ 11.71        -4.286     ]\n     [ -4.286        2.14413333]]\n    >>> print(np.cov(x))\n    11.71\n\n    '
    if ((ddof is not None) and (ddof != int(ddof))):
        raise ValueError('ddof must be integer')
    m = np.asarray(m)
    if (m.ndim > 2):
        raise ValueError('m has more than 2 dimensions')
    if (y is None):
        dtype = np.result_type(m, np.float64)
    else:
        y = np.asarray(y)
        if (y.ndim > 2):
            raise ValueError('y has more than 2 dimensions')
        dtype = np.result_type(m, y, np.float64)
    X = array(m, ndmin=2, dtype=dtype)
    if ((not rowvar) and (X.shape[0] != 1)):
        X = X.T
    if (X.shape[0] == 0):
        return np.array([]).reshape(0, 0)
    if (y is not None):
        y = array(y, copy=False, ndmin=2, dtype=dtype)
        if ((not rowvar) and (y.shape[0] != 1)):
            y = y.T
        X = np.vstack((X, y))
    if (ddof is None):
        if (bias == 0):
            ddof = 1
        else:
            ddof = 0
    w = None
    if (fweights is not None):
        fweights = np.asarray(fweights, dtype=np.float)
        if (not np.all((fweights == np.around(fweights)))):
            raise TypeError('fweights must be integer')
        if (fweights.ndim > 1):
            raise RuntimeError('cannot handle multidimensional fweights')
        if (fweights.shape[0] != X.shape[1]):
            raise RuntimeError('incompatible numbers of samples and fweights')
        if any((fweights < 0)):
            raise ValueError('fweights cannot be negative')
        w = fweights
    if (aweights is not None):
        aweights = np.asarray(aweights, dtype=np.float)
        if (aweights.ndim > 1):
            raise RuntimeError('cannot handle multidimensional aweights')
        if (aweights.shape[0] != X.shape[1]):
            raise RuntimeError('incompatible numbers of samples and aweights')
        if any((aweights < 0)):
            raise ValueError('aweights cannot be negative')
        if (w is None):
            w = aweights
        else:
            w *= aweights
    (avg, w_sum) = average(X, axis=1, weights=w, returned=True)
    w_sum = w_sum[0]
    if (w is None):
        fact = (X.shape[1] - ddof)
    elif (ddof == 0):
        fact = w_sum
    elif (aweights is None):
        fact = (w_sum - ddof)
    else:
        fact = (w_sum - ((ddof * sum((w * aweights))) / w_sum))
    if (fact <= 0):
        warnings.warn('Degrees of freedom <= 0 for slice', RuntimeWarning, stacklevel=2)
        fact = 0.0
    X -= avg[:, None]
    if (w is None):
        X_T = X.T
    else:
        X_T = (X * w).T
    c = dot(X, X_T.conj())
    c *= (1.0 / np.float64(fact))
    return c.squeeze()