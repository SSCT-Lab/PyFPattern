@array_function_dispatch(_solve_dispatcher)
def solve(a, b):
    '\n    Solve a linear matrix equation, or system of linear scalar equations.\n\n    Computes the "exact" solution, `x`, of the well-determined, i.e., full\n    rank, linear matrix equation `ax = b`.\n\n    Parameters\n    ----------\n    a : (..., M, M) array_like\n        Coefficient matrix.\n    b : {(..., M,), (..., M, K)}, array_like\n        Ordinate or "dependent variable" values.\n\n    Returns\n    -------\n    x : {(..., M,), (..., M, K)} ndarray\n        Solution to the system a x = b.  Returned shape is identical to `b`.\n\n    Raises\n    ------\n    LinAlgError\n        If `a` is singular or not square.\n\n    Notes\n    -----\n\n    .. versionadded:: 1.8.0\n\n    Broadcasting rules apply, see the `numpy.linalg` documentation for\n    details.\n\n    The solutions are computed using LAPACK routine ``_gesv``.\n\n    `a` must be square and of full-rank, i.e., all rows (or, equivalently,\n    columns) must be linearly independent; if either is not true, use\n    `lstsq` for the least-squares best "solution" of the\n    system/equation.\n\n    References\n    ----------\n    .. [1] G. Strang, *Linear Algebra and Its Applications*, 2nd Ed., Orlando,\n           FL, Academic Press, Inc., 1980, pg. 22.\n\n    Examples\n    --------\n    Solve the system of equations ``3 * x0 + x1 = 9`` and ``x0 + 2 * x1 = 8``:\n\n    >>> a = np.array([[3,1], [1,2]])\n    >>> b = np.array([9,8])\n    >>> x = np.linalg.solve(a, b)\n    >>> x\n    array([2.,  3.])\n\n    Check that the solution is correct:\n\n    >>> np.allclose(np.dot(a, x), b)\n    True\n\n    '
    (a, _) = _makearray(a)
    _assert_stacked_2d(a)
    _assert_stacked_square(a)
    (b, wrap) = _makearray(b)
    (t, result_t) = _commonType(a, b)
    if (b.ndim == (a.ndim - 1)):
        gufunc = _umath_linalg.solve1
    else:
        gufunc = _umath_linalg.solve
    signature = ('DD->D' if isComplexType(t) else 'dd->d')
    extobj = get_linalg_error_extobj(_raise_linalgerror_singular)
    r = gufunc(a, b, signature=signature, extobj=extobj)
    return wrap(r.astype(result_t, copy=False))