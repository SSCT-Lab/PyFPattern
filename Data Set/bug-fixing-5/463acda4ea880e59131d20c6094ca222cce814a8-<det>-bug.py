@array_function_dispatch(_unary_dispatcher)
def det(a):
    '\n    Compute the determinant of an array.\n\n    Parameters\n    ----------\n    a : (..., M, M) array_like\n        Input array to compute determinants for.\n\n    Returns\n    -------\n    det : (...) array_like\n        Determinant of `a`.\n\n    See Also\n    --------\n    slogdet : Another way to represent the determinant, more suitable\n      for large matrices where underflow/overflow may occur.\n\n    Notes\n    -----\n\n    .. versionadded:: 1.8.0\n\n    Broadcasting rules apply, see the `numpy.linalg` documentation for\n    details.\n\n    The determinant is computed via LU factorization using the LAPACK\n    routine ``z/dgetrf``.\n\n    Examples\n    --------\n    The determinant of a 2-D array [[a, b], [c, d]] is ad - bc:\n\n    >>> a = np.array([[1, 2], [3, 4]])\n    >>> np.linalg.det(a)\n    -2.0 # may vary\n\n    Computing determinants for a stack of matrices:\n\n    >>> a = np.array([ [[1, 2], [3, 4]], [[1, 2], [2, 1]], [[1, 3], [3, 1]] ])\n    >>> a.shape\n    (3, 2, 2)\n    >>> np.linalg.det(a)\n    array([-2., -3., -8.])\n\n    '
    a = asarray(a)
    _assertRankAtLeast2(a)
    _assertNdSquareness(a)
    (t, result_t) = _commonType(a)
    signature = ('D->D' if isComplexType(t) else 'd->d')
    r = _umath_linalg.det(a, signature=signature)
    r = r.astype(result_t, copy=False)
    return r