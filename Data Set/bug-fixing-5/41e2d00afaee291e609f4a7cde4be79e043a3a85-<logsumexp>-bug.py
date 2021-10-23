def logsumexp(a, axis=None, b=None, keepdims=False, return_sign=False):
    'Compute the log of the sum of exponentials of input elements.\n\n    Parameters\n    ----------\n    a : array_like\n        Input array.\n    axis : None or int or tuple of ints, optional\n        Axis or axes over which the sum is taken. By default `axis` is None,\n        and all elements are summed. Tuple of ints is not accepted if NumPy\n        version is lower than 1.7.0.\n\n        .. versionadded:: 0.11.0\n    keepdims : bool, optional\n        If this is set to True, the axes which are reduced are left in the\n        result as dimensions with size one. With this option, the result\n        will broadcast correctly against the original array.\n\n        .. versionadded:: 0.15.0\n    b : array-like, optional\n        Scaling factor for exp(`a`) must be of the same shape as `a` or\n        broadcastable to `a`. These values may be negative in order to\n        implement subtraction.\n\n        .. versionadded:: 0.12.0\n    return_sign : bool, optional\n        If this is set to True, the result will be a pair containing sign\n        information; if False, results that are negative will be returned\n        as NaN. Default is False (no sign information).\n\n        .. versionadded:: 0.16.0\n    Returns\n    -------\n    res : ndarray\n        The result, ``np.log(np.sum(np.exp(a)))`` calculated in a numerically\n        more stable way. If `b` is given then ``np.log(np.sum(b*np.exp(a)))``\n        is returned.\n    sgn : ndarray\n        If return_sign is True, this will be an array of floating-point\n        numbers matching res and +1, 0, or -1 depending on the sign\n        of the result. If False, only one result is returned.\n\n    See Also\n    --------\n    numpy.logaddexp, numpy.logaddexp2\n\n    Notes\n    -----\n    Numpy has a logaddexp function which is very similar to `logsumexp`, but\n    only handles two arguments. `logaddexp.reduce` is similar to this\n    function, but may be less stable.\n\n    Examples\n    --------\n    >>> from scipy.misc import logsumexp\n    >>> a = np.arange(10)\n    >>> np.log(np.sum(np.exp(a)))\n    9.4586297444267107\n    >>> logsumexp(a)\n    9.4586297444267107\n\n    With weights\n\n    >>> a = np.arange(10)\n    >>> b = np.arange(10, 0, -1)\n    >>> logsumexp(a, b=b)\n    9.9170178533034665\n    >>> np.log(np.sum(b*np.exp(a)))\n    9.9170178533034647\n\n    Returning a sign flag\n\n    >>> logsumexp([1,2],b=[1,-1],return_sign=True)\n    (1.5413248546129181, -1.0)\n\n    '
    a = asarray(a)
    if (b is not None):
        (a, b) = broadcast_arrays(a, b)
        if np.any((b == 0)):
            a = (a + 0.0)
            a[(b == 0)] = (- np.inf)
    a_max = amax(a, axis=axis, keepdims=True)
    if (a_max.ndim > 0):
        a_max[(~ isfinite(a_max))] = 0
    elif (not isfinite(a_max)):
        a_max = 0
    if (b is not None):
        b = asarray(b)
        tmp = (b * exp((a - a_max)))
    else:
        tmp = exp((a - a_max))
    with np.errstate(divide='ignore'):
        s = sum(tmp, axis=axis, keepdims=keepdims)
        if return_sign:
            sgn = sign(s)
            s *= sgn
        out = log(s)
    if (not keepdims):
        a_max = squeeze(a_max, axis=axis)
    out += a_max
    if return_sign:
        return (out, sgn)
    else:
        return out