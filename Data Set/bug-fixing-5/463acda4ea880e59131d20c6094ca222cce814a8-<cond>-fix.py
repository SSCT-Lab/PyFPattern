@array_function_dispatch(_cond_dispatcher)
def cond(x, p=None):
    "\n    Compute the condition number of a matrix.\n\n    This function is capable of returning the condition number using\n    one of seven different norms, depending on the value of `p` (see\n    Parameters below).\n\n    Parameters\n    ----------\n    x : (..., M, N) array_like\n        The matrix whose condition number is sought.\n    p : {None, 1, -1, 2, -2, inf, -inf, 'fro'}, optional\n        Order of the norm:\n\n        =====  ============================\n        p      norm for matrices\n        =====  ============================\n        None   2-norm, computed directly using the ``SVD``\n        'fro'  Frobenius norm\n        inf    max(sum(abs(x), axis=1))\n        -inf   min(sum(abs(x), axis=1))\n        1      max(sum(abs(x), axis=0))\n        -1     min(sum(abs(x), axis=0))\n        2      2-norm (largest sing. value)\n        -2     smallest singular value\n        =====  ============================\n\n        inf means the numpy.inf object, and the Frobenius norm is\n        the root-of-sum-of-squares norm.\n\n    Returns\n    -------\n    c : {float, inf}\n        The condition number of the matrix. May be infinite.\n\n    See Also\n    --------\n    numpy.linalg.norm\n\n    Notes\n    -----\n    The condition number of `x` is defined as the norm of `x` times the\n    norm of the inverse of `x` [1]_; the norm can be the usual L2-norm\n    (root-of-sum-of-squares) or one of a number of other matrix norms.\n\n    References\n    ----------\n    .. [1] G. Strang, *Linear Algebra and Its Applications*, Orlando, FL,\n           Academic Press, Inc., 1980, pg. 285.\n\n    Examples\n    --------\n    >>> from numpy import linalg as LA\n    >>> a = np.array([[1, 0, -1], [0, 1, 0], [1, 0, 1]])\n    >>> a\n    array([[ 1,  0, -1],\n           [ 0,  1,  0],\n           [ 1,  0,  1]])\n    >>> LA.cond(a)\n    1.4142135623730951\n    >>> LA.cond(a, 'fro')\n    3.1622776601683795\n    >>> LA.cond(a, np.inf)\n    2.0\n    >>> LA.cond(a, -np.inf)\n    1.0\n    >>> LA.cond(a, 1)\n    2.0\n    >>> LA.cond(a, -1)\n    1.0\n    >>> LA.cond(a, 2)\n    1.4142135623730951\n    >>> LA.cond(a, -2)\n    0.70710678118654746 # may vary\n    >>> min(LA.svd(a, compute_uv=False))*min(LA.svd(LA.inv(a), compute_uv=False))\n    0.70710678118654746 # may vary\n\n    "
    x = asarray(x)
    if _is_empty_2d(x):
        raise LinAlgError('cond is not defined on empty arrays')
    if ((p is None) or (p == 2) or (p == (- 2))):
        s = svd(x, compute_uv=False)
        with errstate(all='ignore'):
            if (p == (- 2)):
                r = (s[(..., (- 1))] / s[(..., 0)])
            else:
                r = (s[(..., 0)] / s[(..., (- 1))])
    else:
        _assert_stacked_2d(x)
        _assert_stacked_square(x)
        (t, result_t) = _commonType(x)
        signature = ('D->D' if isComplexType(t) else 'd->d')
        with errstate(all='ignore'):
            invx = _umath_linalg.inv(x, signature=signature)
            r = (norm(x, p, axis=((- 2), (- 1))) * norm(invx, p, axis=((- 2), (- 1))))
        r = r.astype(result_t, copy=False)
    r = asarray(r)
    nan_mask = isnan(r)
    if nan_mask.any():
        nan_mask &= (~ isnan(x).any(axis=((- 2), (- 1))))
        if (r.ndim > 0):
            r[nan_mask] = Inf
        elif nan_mask:
            r[()] = Inf
    if (r.ndim == 0):
        r = r[()]
    return r