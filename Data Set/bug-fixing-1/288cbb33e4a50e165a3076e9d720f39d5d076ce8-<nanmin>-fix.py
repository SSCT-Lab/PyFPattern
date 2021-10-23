

def nanmin(a, axis=None, out=None, keepdims=np._NoValue):
    '\n    Return minimum of an array or minimum along an axis, ignoring any NaNs.\n    When all-NaN slices are encountered a ``RuntimeWarning`` is raised and\n    Nan is returned for that slice.\n\n    Parameters\n    ----------\n    a : array_like\n        Array containing numbers whose minimum is desired. If `a` is not an\n        array, a conversion is attempted.\n    axis : int, optional\n        Axis along which the minimum is computed. The default is to compute\n        the minimum of the flattened array.\n    out : ndarray, optional\n        Alternate output array in which to place the result.  The default\n        is ``None``; if provided, it must have the same shape as the\n        expected output, but the type will be cast if necessary.  See\n        `doc.ufuncs` for details.\n\n        .. versionadded:: 1.8.0\n    keepdims : bool, optional\n        If this is set to True, the axes which are reduced are left\n        in the result as dimensions with size one. With this option,\n        the result will broadcast correctly against the original `a`.\n\n        If the value is anything but the default, then\n        `keepdims` will be passed through to the `min` method\n        of sub-classes of `ndarray`.  If the sub-classes methods\n        does not implement `keepdims` any exceptions will be raised.\n\n        .. versionadded:: 1.8.0\n\n    Returns\n    -------\n    nanmin : ndarray\n        An array with the same shape as `a`, with the specified axis\n        removed.  If `a` is a 0-d array, or if axis is None, an ndarray\n        scalar is returned.  The same dtype as `a` is returned.\n\n    See Also\n    --------\n    nanmax :\n        The maximum value of an array along a given axis, ignoring any NaNs.\n    amin :\n        The minimum value of an array along a given axis, propagating any NaNs.\n    fmin :\n        Element-wise minimum of two arrays, ignoring any NaNs.\n    minimum :\n        Element-wise minimum of two arrays, propagating any NaNs.\n    isnan :\n        Shows which elements are Not a Number (NaN).\n    isfinite:\n        Shows which elements are neither NaN nor infinity.\n\n    amax, fmax, maximum\n\n    Notes\n    -----\n    NumPy uses the IEEE Standard for Binary Floating-Point for Arithmetic\n    (IEEE 754). This means that Not a Number is not equivalent to infinity.\n    Positive infinity is treated as a very large number and negative\n    infinity is treated as a very small (i.e. negative) number.\n\n    If the input has a integer type the function is equivalent to np.min.\n\n    Examples\n    --------\n    >>> a = np.array([[1, 2], [3, np.nan]])\n    >>> np.nanmin(a)\n    1.0\n    >>> np.nanmin(a, axis=0)\n    array([ 1.,  2.])\n    >>> np.nanmin(a, axis=1)\n    array([ 1.,  3.])\n\n    When positive infinity and negative infinity are present:\n\n    >>> np.nanmin([1, 2, np.nan, np.inf])\n    1.0\n    >>> np.nanmin([1, 2, np.nan, np.NINF])\n    -inf\n\n    '
    kwargs = {
        
    }
    if (keepdims is not np._NoValue):
        kwargs['keepdims'] = keepdims
    if ((type(a) is np.ndarray) and (a.dtype != np.object_)):
        res = np.fmin.reduce(a, axis=axis, out=out, **kwargs)
        if np.isnan(res).any():
            warnings.warn('All-NaN slice encountered', RuntimeWarning, stacklevel=2)
    else:
        (a, mask) = _replace_nan(a, (+ np.inf))
        res = np.amin(a, axis=axis, out=out, **kwargs)
        if (mask is None):
            return res
        mask = np.all(mask, axis=axis, **kwargs)
        if np.any(mask):
            res = _copyto(res, np.nan, mask)
            warnings.warn('All-NaN axis encountered', RuntimeWarning, stacklevel=2)
    return res
