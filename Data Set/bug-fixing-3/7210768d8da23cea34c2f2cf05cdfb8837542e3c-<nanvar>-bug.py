def nanvar(a, axis=None, dtype=None, out=None, ddof=0, keepdims=np._NoValue):
    '\n    Compute the variance along the specified axis, while ignoring NaNs.\n\n    Returns the variance of the array elements, a measure of the spread of\n    a distribution.  The variance is computed for the flattened array by\n    default, otherwise over the specified axis.\n\n    For all-NaN slices or slices with zero degrees of freedom, NaN is\n    returned and a `RuntimeWarning` is raised.\n\n    .. versionadded:: 1.8.0\n\n    Parameters\n    ----------\n    a : array_like\n        Array containing numbers whose variance is desired.  If `a` is not an\n        array, a conversion is attempted.\n    axis : int, optional\n        Axis along which the variance is computed.  The default is to compute\n        the variance of the flattened array.\n    dtype : data-type, optional\n        Type to use in computing the variance.  For arrays of integer type\n        the default is `float32`; for arrays of float types it is the same as\n        the array type.\n    out : ndarray, optional\n        Alternate output array in which to place the result.  It must have\n        the same shape as the expected output, but the type is cast if\n        necessary.\n    ddof : int, optional\n        "Delta Degrees of Freedom": the divisor used in the calculation is\n        ``N - ddof``, where ``N`` represents the number of non-NaN\n        elements. By default `ddof` is zero.\n    keepdims : bool, optional\n        If this is set to True, the axes which are reduced are left\n        in the result as dimensions with size one. With this option,\n        the result will broadcast correctly against the original `a`.\n\n\n    Returns\n    -------\n    variance : ndarray, see dtype parameter above\n        If `out` is None, return a new array containing the variance,\n        otherwise return a reference to the output array. If ddof is >= the\n        number of non-NaN elements in a slice or the slice contains only\n        NaNs, then the result for that slice is NaN.\n\n    See Also\n    --------\n    std : Standard deviation\n    mean : Average\n    var : Variance while not ignoring NaNs\n    nanstd, nanmean\n    numpy.doc.ufuncs : Section "Output arguments"\n\n    Notes\n    -----\n    The variance is the average of the squared deviations from the mean,\n    i.e.,  ``var = mean(abs(x - x.mean())**2)``.\n\n    The mean is normally calculated as ``x.sum() / N``, where ``N = len(x)``.\n    If, however, `ddof` is specified, the divisor ``N - ddof`` is used\n    instead.  In standard statistical practice, ``ddof=1`` provides an\n    unbiased estimator of the variance of a hypothetical infinite\n    population.  ``ddof=0`` provides a maximum likelihood estimate of the\n    variance for normally distributed variables.\n\n    Note that for complex numbers, the absolute value is taken before\n    squaring, so that the result is always real and nonnegative.\n\n    For floating-point input, the variance is computed using the same\n    precision the input has.  Depending on the input data, this can cause\n    the results to be inaccurate, especially for `float32` (see example\n    below).  Specifying a higher-accuracy accumulator using the ``dtype``\n    keyword can alleviate this issue.\n\n    For this function to work on sub-classes of ndarray, they must define\n    `sum` with the kwarg `keepdims`\n\n    Examples\n    --------\n    >>> a = np.array([[1, np.nan], [3, 4]])\n    >>> np.var(a)\n    1.5555555555555554\n    >>> np.nanvar(a, axis=0)\n    array([ 1.,  0.])\n    >>> np.nanvar(a, axis=1)\n    array([ 0.,  0.25])\n\n    '
    (arr, mask) = _replace_nan(a, 0)
    if (mask is None):
        return np.var(arr, axis=axis, dtype=dtype, out=out, ddof=ddof, keepdims=keepdims)
    if (dtype is not None):
        dtype = np.dtype(dtype)
    if ((dtype is not None) and (not issubclass(dtype.type, np.inexact))):
        raise TypeError('If a is inexact, then dtype must be inexact')
    if ((out is not None) and (not issubclass(out.dtype.type, np.inexact))):
        raise TypeError('If a is inexact, then out must be inexact')
    if (type(arr) is np.matrix):
        _keepdims = np._NoValue
    else:
        _keepdims = True
    cnt = np.sum((~ mask), axis=axis, dtype=np.intp, keepdims=_keepdims)
    avg = np.sum(arr, axis=axis, dtype=dtype, keepdims=_keepdims)
    avg = _divide_by_count(avg, cnt)
    np.subtract(arr, avg, out=arr, casting='unsafe')
    arr = _copyto(arr, 0, mask)
    if issubclass(arr.dtype.type, np.complexfloating):
        sqr = np.multiply(arr, arr.conj(), out=arr).real
    else:
        sqr = np.multiply(arr, arr, out=arr)
    var = np.sum(sqr, axis=axis, dtype=dtype, out=out, keepdims=keepdims)
    if (var.ndim < cnt.ndim):
        cnt = cnt.squeeze(axis)
    dof = (cnt - ddof)
    var = _divide_by_count(var, dof)
    isbad = (dof <= 0)
    if np.any(isbad):
        warnings.warn('Degrees of freedom <= 0 for slice.', RuntimeWarning, stacklevel=2)
        var = _copyto(var, np.nan, isbad)
    return var