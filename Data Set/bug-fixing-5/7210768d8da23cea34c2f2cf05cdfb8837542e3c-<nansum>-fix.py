def nansum(a, axis=None, dtype=None, out=None, keepdims=np._NoValue):
    '\n    Return the sum of array elements over a given axis treating Not a\n    Numbers (NaNs) as zero.\n\n    In NumPy versions <= 1.9.0 Nan is returned for slices that are all-NaN or\n    empty. In later versions zero is returned.\n\n    Parameters\n    ----------\n    a : array_like\n        Array containing numbers whose sum is desired. If `a` is not an\n        array, a conversion is attempted.\n    axis : {int, tuple of int, None}, optional\n        Axis or axes along which the sum is computed. The default is to compute the\n        sum of the flattened array.\n    dtype : data-type, optional\n        The type of the returned array and of the accumulator in which the\n        elements are summed.  By default, the dtype of `a` is used.  An\n        exception is when `a` has an integer type with less precision than\n        the platform (u)intp. In that case, the default will be either\n        (u)int32 or (u)int64 depending on whether the platform is 32 or 64\n        bits. For inexact inputs, dtype must be inexact.\n\n        .. versionadded:: 1.8.0\n    out : ndarray, optional\n        Alternate output array in which to place the result.  The default\n        is ``None``. If provided, it must have the same shape as the\n        expected output, but the type will be cast if necessary.  See\n        `doc.ufuncs` for details. The casting of NaN to integer can yield\n        unexpected results.\n\n        .. versionadded:: 1.8.0\n    keepdims : bool, optional\n        If this is set to True, the axes which are reduced are left\n        in the result as dimensions with size one. With this option,\n        the result will broadcast correctly against the original `a`.\n\n\n        If the value is anything but the default, then\n        `keepdims` will be passed through to the `mean` or `sum` methods\n        of sub-classes of `ndarray`.  If the sub-classes methods\n        does not implement `keepdims` any exceptions will be raised.\n\n        .. versionadded:: 1.8.0\n\n    Returns\n    -------\n    nansum : ndarray.\n        A new array holding the result is returned unless `out` is\n        specified, in which it is returned. The result has the same\n        size as `a`, and the same shape as `a` if `axis` is not None\n        or `a` is a 1-d array.\n\n    See Also\n    --------\n    numpy.sum : Sum across array propagating NaNs.\n    isnan : Show which elements are NaN.\n    isfinite: Show which elements are not NaN or +/-inf.\n\n    Notes\n    -----\n    If both positive and negative infinity are present, the sum will be Not\n    A Number (NaN).\n\n    Examples\n    --------\n    >>> np.nansum(1)\n    1\n    >>> np.nansum([1])\n    1\n    >>> np.nansum([1, np.nan])\n    1.0\n    >>> a = np.array([[1, 1], [1, np.nan]])\n    >>> np.nansum(a)\n    3.0\n    >>> np.nansum(a, axis=0)\n    array([ 2.,  1.])\n    >>> np.nansum([1, np.nan, np.inf])\n    inf\n    >>> np.nansum([1, np.nan, np.NINF])\n    -inf\n    >>> np.nansum([1, np.nan, np.inf, -np.inf]) # both +/- infinity present\n    nan\n\n    '
    (a, mask) = _replace_nan(a, 0)
    return np.sum(a, axis=axis, dtype=dtype, out=out, keepdims=keepdims)