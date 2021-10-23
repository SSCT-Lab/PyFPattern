

def average(a, axis=None, weights=None, returned=False):
    '\n    Compute the weighted average along the specified axis.\n\n    Parameters\n    ----------\n    a : array_like\n        Array containing data to be averaged. If `a` is not an array, a\n        conversion is attempted.\n    axis : int, optional\n        Axis along which to average `a`. If `None`, averaging is done over\n        the flattened array.\n    weights : array_like, optional\n        An array of weights associated with the values in `a`. Each value in\n        `a` contributes to the average according to its associated weight.\n        The weights array can either be 1-D (in which case its length must be\n        the size of `a` along the given axis) or of the same shape as `a`.\n        If `weights=None`, then all data in `a` are assumed to have a\n        weight equal to one.\n    returned : bool, optional\n        Default is `False`. If `True`, the tuple (`average`, `sum_of_weights`)\n        is returned, otherwise only the average is returned.\n        If `weights=None`, `sum_of_weights` is equivalent to the number of\n        elements over which the average is taken.\n\n\n    Returns\n    -------\n    average, [sum_of_weights] : array_type or double\n        Return the average along the specified axis. When returned is `True`,\n        return a tuple with the average as the first element and the sum\n        of the weights as the second element. The return type is `Float`\n        if `a` is of integer type, otherwise it is of the same type as `a`.\n        `sum_of_weights` is of the same type as `average`.\n\n    Raises\n    ------\n    ZeroDivisionError\n        When all weights along axis are zero. See `numpy.ma.average` for a\n        version robust to this type of error.\n    TypeError\n        When the length of 1D `weights` is not the same as the shape of `a`\n        along axis.\n\n    See Also\n    --------\n    mean\n\n    ma.average : average for masked arrays -- useful if your data contains\n                 "missing" values\n\n    Examples\n    --------\n    >>> data = range(1,5)\n    >>> data\n    [1, 2, 3, 4]\n    >>> np.average(data)\n    2.5\n    >>> np.average(range(1,11), weights=range(10,0,-1))\n    4.0\n\n    >>> data = np.arange(6).reshape((3,2))\n    >>> data\n    array([[0, 1],\n           [2, 3],\n           [4, 5]])\n    >>> np.average(data, axis=1, weights=[1./4, 3./4])\n    array([ 0.75,  2.75,  4.75])\n    >>> np.average(data, weights=[1./4, 3./4])\n    Traceback (most recent call last):\n    ...\n    TypeError: Axis must be specified when shapes of a and weights differ.\n\n    '
    a = np.asanyarray(a)
    if (weights is None):
        avg = a.mean(axis)
        scl = avg.dtype.type((a.size / avg.size))
    else:
        wgt = np.asanyarray(weights)
        if issubclass(a.dtype.type, (np.integer, np.bool_)):
            result_dtype = np.result_type(a.dtype, wgt.dtype, 'f8')
        else:
            result_dtype = np.result_type(a.dtype, wgt.dtype)
        if (a.shape != wgt.shape):
            if (axis is None):
                raise TypeError('Axis must be specified when shapes of a and weights differ.')
            if (wgt.ndim != 1):
                raise TypeError('1D weights expected when shapes of a and weights differ.')
            if (wgt.shape[0] != a.shape[axis]):
                raise ValueError('Length of weights not compatible with specified axis.')
            wgt = np.broadcast_to(wgt, (((a.ndim - 1) * (1,)) + wgt.shape))
            wgt = wgt.swapaxes((- 1), axis)
        scl = wgt.sum(axis=axis, dtype=result_dtype)
        if (scl == 0.0).any():
            raise ZeroDivisionError("Weights sum to zero, can't be normalized")
        avg = (np.multiply(a, wgt, dtype=result_dtype).sum(axis) / scl)
    if returned:
        scl = np.broadcast_to(scl, avg.shape)
        return (avg, scl)
    else:
        return avg
