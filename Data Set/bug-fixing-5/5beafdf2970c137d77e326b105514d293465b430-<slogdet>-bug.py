def slogdet(a):
    '\n    Compute the sign and (natural) logarithm of the determinant of an array.\n\n    If an array has a very small or very large determinant, then a call to\n    `det` may overflow or underflow. This routine is more robust against such\n    issues, because it computes the logarithm of the determinant rather than\n    the determinant itself.\n\n    Parameters\n    ----------\n    a : (..., M, M) array_like\n        Input array, has to be a square 2-D array.\n\n    Returns\n    -------\n    sign : (...) array_like\n        A number representing the sign of the determinant. For a real matrix,\n        this is 1, 0, or -1. For a complex matrix, this is a complex number\n        with absolute value 1 (i.e., it is on the unit circle), or else 0.\n    logdet : (...) array_like\n        The natural log of the absolute value of the determinant.\n\n    If the determinant is zero, then `sign` will be 0 and `logdet` will be\n    -Inf. In all cases, the determinant is equal to ``sign * np.exp(logdet)``.\n\n    See Also\n    --------\n    det\n\n    Notes\n    -----\n\n    .. versionadded:: 1.8.0\n\n    Broadcasting rules apply, see the `numpy.linalg` documentation for\n    details.\n\n    .. versionadded:: 1.6.0\n\n    The determinant is computed via LU factorization using the LAPACK\n    routine z/dgetrf.\n\n\n    Examples\n    --------\n    The determinant of a 2-D array ``[[a, b], [c, d]]`` is ``ad - bc``:\n\n    >>> a = np.array([[1, 2], [3, 4]])\n    >>> (sign, logdet) = np.linalg.slogdet(a)\n    >>> (sign, logdet)\n    (-1, 0.69314718055994529)\n    >>> sign * np.exp(logdet)\n    -2.0\n\n    Computing log-determinants for a stack of matrices:\n\n    >>> a = np.array([ [[1, 2], [3, 4]], [[1, 2], [2, 1]], [[1, 3], [3, 1]] ])\n    >>> a.shape\n    (3, 2, 2)\n    >>> sign, logdet = np.linalg.slogdet(a)\n    >>> (sign, logdet)\n    (array([-1., -1., -1.]), array([ 0.69314718,  1.09861229,  2.07944154]))\n    >>> sign * np.exp(logdet)\n    array([-2., -3., -8.])\n\n    This routine succeeds where ordinary `det` does not:\n\n    >>> np.linalg.det(np.eye(500) * 0.1)\n    0.0\n    >>> np.linalg.slogdet(np.eye(500) * 0.1)\n    (1, -1151.2925464970228)\n\n    '
    a = asarray(a)
    _assertRankAtLeast2(a)
    _assertNdSquareness(a)
    (t, result_t) = _commonType(a)
    real_t = _realType(result_t)
    signature = ('D->Dd' if isComplexType(t) else 'd->dd')
    (sign, logdet) = _umath_linalg.slogdet(a, signature=signature)
    if isscalar(sign):
        sign = sign.astype(result_t)
    else:
        sign = sign.astype(result_t, copy=False)
    if isscalar(logdet):
        logdet = logdet.astype(real_t)
    else:
        logdet = logdet.astype(real_t, copy=False)
    return (sign, logdet)