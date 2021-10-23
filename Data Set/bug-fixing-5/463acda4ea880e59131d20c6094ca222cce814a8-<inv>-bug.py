@array_function_dispatch(_unary_dispatcher)
def inv(a):
    '\n    Compute the (multiplicative) inverse of a matrix.\n\n    Given a square matrix `a`, return the matrix `ainv` satisfying\n    ``dot(a, ainv) = dot(ainv, a) = eye(a.shape[0])``.\n\n    Parameters\n    ----------\n    a : (..., M, M) array_like\n        Matrix to be inverted.\n\n    Returns\n    -------\n    ainv : (..., M, M) ndarray or matrix\n        (Multiplicative) inverse of the matrix `a`.\n\n    Raises\n    ------\n    LinAlgError\n        If `a` is not square or inversion fails.\n\n    Notes\n    -----\n\n    .. versionadded:: 1.8.0\n\n    Broadcasting rules apply, see the `numpy.linalg` documentation for\n    details.\n\n    Examples\n    --------\n    >>> from numpy.linalg import inv\n    >>> a = np.array([[1., 2.], [3., 4.]])\n    >>> ainv = inv(a)\n    >>> np.allclose(np.dot(a, ainv), np.eye(2))\n    True\n    >>> np.allclose(np.dot(ainv, a), np.eye(2))\n    True\n\n    If a is a matrix object, then the return value is a matrix as well:\n\n    >>> ainv = inv(np.matrix(a))\n    >>> ainv\n    matrix([[-2. ,  1. ],\n            [ 1.5, -0.5]])\n\n    Inverses of several matrices can be computed at once:\n\n    >>> a = np.array([[[1., 2.], [3., 4.]], [[1, 3], [3, 5]]])\n    >>> inv(a)\n    array([[[-2.  ,  1.  ],\n            [ 1.5 , -0.5 ]],\n           [[-1.25,  0.75],\n            [ 0.75, -0.25]]])\n\n    '
    (a, wrap) = _makearray(a)
    _assertRankAtLeast2(a)
    _assertNdSquareness(a)
    (t, result_t) = _commonType(a)
    signature = ('D->D' if isComplexType(t) else 'd->d')
    extobj = get_linalg_error_extobj(_raise_linalgerror_singular)
    ainv = _umath_linalg.inv(a, signature=signature, extobj=extobj)
    return wrap(ainv.astype(result_t, copy=False))