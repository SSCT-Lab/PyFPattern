@array_function_dispatch(_lstsq_dispatcher)
def lstsq(a, b, rcond='warn'):
    '\n    Return the least-squares solution to a linear matrix equation.\n\n    Solves the equation :math:`a x = b` by computing a vector `x` that\n    minimizes the squared Euclidean 2-norm :math:`\\| b - a x \\|^2_2`.\n    The equation may be under-, well-, or over-determined (i.e., the\n    number of linearly independent rows of `a` can be less than, equal\n    to, or greater than its number of linearly independent columns).\n    If `a` is square and of full rank, then `x` (but for round-off error)\n    is the "exact" solution of the equation.\n\n    Parameters\n    ----------\n    a : (M, N) array_like\n        "Coefficient" matrix.\n    b : {(M,), (M, K)} array_like\n        Ordinate or "dependent variable" values. If `b` is two-dimensional,\n        the least-squares solution is calculated for each of the `K` columns\n        of `b`.\n    rcond : float, optional\n        Cut-off ratio for small singular values of `a`.\n        For the purposes of rank determination, singular values are treated\n        as zero if they are smaller than `rcond` times the largest singular\n        value of `a`.\n\n        .. versionchanged:: 1.14.0\n           If not set, a FutureWarning is given. The previous default\n           of ``-1`` will use the machine precision as `rcond` parameter,\n           the new default will use the machine precision times `max(M, N)`.\n           To silence the warning and use the new default, use ``rcond=None``,\n           to keep using the old behavior, use ``rcond=-1``.\n\n    Returns\n    -------\n    x : {(N,), (N, K)} ndarray\n        Least-squares solution. If `b` is two-dimensional,\n        the solutions are in the `K` columns of `x`.\n    residuals : {(1,), (K,), (0,)} ndarray\n        Sums of residuals; squared Euclidean 2-norm for each column in\n        ``b - a*x``.\n        If the rank of `a` is < N or M <= N, this is an empty array.\n        If `b` is 1-dimensional, this is a (1,) shape array.\n        Otherwise the shape is (K,).\n    rank : int\n        Rank of matrix `a`.\n    s : (min(M, N),) ndarray\n        Singular values of `a`.\n\n    Raises\n    ------\n    LinAlgError\n        If computation does not converge.\n\n    Notes\n    -----\n    If `b` is a matrix, then all array results are returned as matrices.\n\n    Examples\n    --------\n    Fit a line, ``y = mx + c``, through some noisy data-points:\n\n    >>> x = np.array([0, 1, 2, 3])\n    >>> y = np.array([-1, 0.2, 0.9, 2.1])\n\n    By examining the coefficients, we see that the line should have a\n    gradient of roughly 1 and cut the y-axis at, more or less, -1.\n\n    We can rewrite the line equation as ``y = Ap``, where ``A = [[x 1]]``\n    and ``p = [[m], [c]]``.  Now use `lstsq` to solve for `p`:\n\n    >>> A = np.vstack([x, np.ones(len(x))]).T\n    >>> A\n    array([[ 0.,  1.],\n           [ 1.,  1.],\n           [ 2.,  1.],\n           [ 3.,  1.]])\n\n    >>> m, c = np.linalg.lstsq(A, y, rcond=None)[0]\n    >>> m, c\n    (1.0 -0.95) # may vary\n\n    Plot the data along with the fitted line:\n\n    >>> import matplotlib.pyplot as plt\n    >>> _ = plt.plot(x, y, \'o\', label=\'Original data\', markersize=10)\n    >>> _ = plt.plot(x, m*x + c, \'r\', label=\'Fitted line\')\n    >>> _ = plt.legend()\n    >>> plt.show()\n\n    '
    (a, _) = _makearray(a)
    (b, wrap) = _makearray(b)
    is_1d = (b.ndim == 1)
    if is_1d:
        b = b[:, newaxis]
    _assertRank2(a, b)
    (m, n) = a.shape[(- 2):]
    (m2, n_rhs) = b.shape[(- 2):]
    if (m != m2):
        raise LinAlgError('Incompatible dimensions')
    (t, result_t) = _commonType(a, b)
    real_t = _linalgRealType(t)
    result_real_t = _realType(result_t)
    if (rcond == 'warn'):
        warnings.warn('`rcond` parameter will change to the default of machine precision times ``max(M, N)`` where M and N are the input matrix dimensions.\nTo use the future default and silence this warning we advise to pass `rcond=None`, to keep using the old, explicitly pass `rcond=-1`.', FutureWarning, stacklevel=2)
        rcond = (- 1)
    if (rcond is None):
        rcond = (finfo(t).eps * max(n, m))
    if (m <= n):
        gufunc = _umath_linalg.lstsq_m
    else:
        gufunc = _umath_linalg.lstsq_n
    signature = ('DDd->Ddid' if isComplexType(t) else 'ddd->ddid')
    extobj = get_linalg_error_extobj(_raise_linalgerror_lstsq)
    if (n_rhs == 0):
        b = zeros((b.shape[:(- 2)] + (m, (n_rhs + 1))), dtype=b.dtype)
    (x, resids, rank, s) = gufunc(a, b, rcond, signature=signature, extobj=extobj)
    if (m == 0):
        x[...] = 0
    if (n_rhs == 0):
        x = x[..., :n_rhs]
        resids = resids[..., :n_rhs]
    if is_1d:
        x = x.squeeze(axis=(- 1))
    if ((rank != n) or (m <= n)):
        resids = array([], result_real_t)
    s = s.astype(result_real_t, copy=False)
    resids = resids.astype(result_real_t, copy=False)
    x = x.astype(result_t, copy=True)
    return (wrap(x), wrap(resids), rank, s)