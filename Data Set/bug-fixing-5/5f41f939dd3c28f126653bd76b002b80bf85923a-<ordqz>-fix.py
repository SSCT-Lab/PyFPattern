def ordqz(A, B, sort='lhp', output='real', overwrite_a=False, overwrite_b=False, check_finite=True):
    "QZ decomposition for a pair of matrices with reordering.\n\n    .. versionadded:: 0.17.0\n\n    Parameters\n    ----------\n    A : (N, N) array_like\n        2d array to decompose\n    B : (N, N) array_like\n        2d array to decompose\n    sort : {callable, 'lhp', 'rhp', 'iuc', 'ouc'}, optional\n        Specifies whether the upper eigenvalues should be sorted. A\n        callable may be passed that, given an ordered pair ``(alpha,\n        beta)`` representing the eigenvalue ``x = (alpha/beta)``,\n        returns a boolean denoting whether the eigenvalue should be\n        sorted to the top-left (True). For the real matrix pairs\n        ``beta`` is real while ``alpha`` can be complex, and for\n        complex matrix pairs both ``alpha`` and ``beta`` can be\n        complex. The callable must be able to accept a numpy\n        array. Alternatively, string parameters may be used:\n\n            - 'lhp'   Left-hand plane (x.real < 0.0)\n            - 'rhp'   Right-hand plane (x.real > 0.0)\n            - 'iuc'   Inside the unit circle (x*x.conjugate() < 1.0)\n            - 'ouc'   Outside the unit circle (x*x.conjugate() > 1.0)\n\n        With the predefined sorting functions, an infinite eigenvalue\n        (i.e. ``alpha != 0`` and ``beta = 0``) is considered to lie in\n        neither the left-hand nor the right-hand plane, but it is\n        considered to lie outside the unit circle. For the eigenvalue\n        ``(alpha, beta) = (0, 0)`` the predefined sorting functions\n        all return `False`.\n\n    output : str {'real','complex'}, optional\n        Construct the real or complex QZ decomposition for real matrices.\n        Default is 'real'.\n    overwrite_a : bool, optional\n        If True, the contents of A are overwritten.\n    overwrite_b : bool, optional\n        If True, the contents of B are overwritten.\n    check_finite : bool, optional\n        If true checks the elements of `A` and `B` are finite numbers. If\n        false does no checking and passes matrix through to\n        underlying algorithm.\n\n    Returns\n    -------\n    AA : (N, N) ndarray\n        Generalized Schur form of A.\n    BB : (N, N) ndarray\n        Generalized Schur form of B.\n    alpha : (N,) ndarray\n        alpha = alphar + alphai * 1j. See notes.\n    beta : (N,) ndarray\n        See notes.\n    Q : (N, N) ndarray\n        The left Schur vectors.\n    Z : (N, N) ndarray\n        The right Schur vectors.\n\n    Notes\n    -----\n    On exit, ``(ALPHAR(j) + ALPHAI(j)*i)/BETA(j), j=1,...,N``, will be the\n    generalized eigenvalues.  ``ALPHAR(j) + ALPHAI(j)*i`` and\n    ``BETA(j),j=1,...,N`` are the diagonals of the complex Schur form (S,T)\n    that would result if the 2-by-2 diagonal blocks of the real generalized\n    Schur form of (A,B) were further reduced to triangular form using complex\n    unitary transformations. If ALPHAI(j) is zero, then the j-th eigenvalue is\n    real; if positive, then the ``j``-th and ``(j+1)``-st eigenvalues are a\n    complex conjugate pair, with ``ALPHAI(j+1)`` negative.\n\n    See also\n    --------\n    qz\n\n    "
    lwork = None
    (result, typ) = _qz(A, B, output=output, lwork=lwork, sort=None, overwrite_a=overwrite_a, overwrite_b=overwrite_b, check_finite=check_finite)
    (AA, BB, Q, Z) = (result[0], result[1], result[(- 4)], result[(- 3)])
    if (typ not in 'cz'):
        (alpha, beta) = ((result[3] + (result[4] * 1j)), result[5])
    else:
        (alpha, beta) = (result[3], result[4])
    sfunction = _select_function(sort)
    select = sfunction(alpha, beta)
    (tgsen,) = get_lapack_funcs(('tgsen',), (AA, BB))
    if ((lwork is None) or (lwork == (- 1))):
        result = tgsen(select, AA, BB, Q, Z, lwork=(- 1))
        lwork = result[(- 3)][0].real.astype(np.int)
        lwork += 1
    liwork = None
    if ((liwork is None) or (liwork == (- 1))):
        result = tgsen(select, AA, BB, Q, Z, liwork=(- 1))
        liwork = result[(- 2)][0]
    result = tgsen(select, AA, BB, Q, Z, lwork=lwork, liwork=liwork)
    info = result[(- 1)]
    if (info < 0):
        raise ValueError(('Illegal value in argument %d of tgsen' % (- info)))
    elif (info == 1):
        raise ValueError('Reordering of (A, B) failed because the transformed matrix pair (A, B) would be too far from generalized Schur form; the problem is very ill-conditioned. (A, B) may have been partially reorded. If requested, 0 is returned in DIF(*), PL, and PR.')
    if (typ in ['f', 'd']):
        alpha = (result[2] + (result[3] * 1j))
        return (result[0], result[1], alpha, result[4], result[5], result[6])
    else:
        return (result[0], result[1], result[2], result[3], result[4], result[5])