@array_function_dispatch(_svd_dispatcher)
def svd(a, full_matrices=True, compute_uv=True, hermitian=False):
    '\n    Singular Value Decomposition.\n\n    When `a` is a 2D array, it is factorized as ``u @ np.diag(s) @ vh\n    = (u * s) @ vh``, where `u` and `vh` are 2D unitary arrays and `s` is a 1D\n    array of `a`\'s singular values. When `a` is higher-dimensional, SVD is\n    applied in stacked mode as explained below.\n\n    Parameters\n    ----------\n    a : (..., M, N) array_like\n        A real or complex array with ``a.ndim >= 2``.\n    full_matrices : bool, optional\n        If True (default), `u` and `vh` have the shapes ``(..., M, M)`` and\n        ``(..., N, N)``, respectively.  Otherwise, the shapes are\n        ``(..., M, K)`` and ``(..., K, N)``, respectively, where\n        ``K = min(M, N)``.\n    compute_uv : bool, optional\n        Whether or not to compute `u` and `vh` in addition to `s`.  True\n        by default.\n    hermitian : bool, optional\n        If True, `a` is assumed to be Hermitian (symmetric if real-valued),\n        enabling a more efficient method for finding singular values.\n        Defaults to False.\n\n        .. versionadded:: 1.17.0\n\n    Returns\n    -------\n    u : { (..., M, M), (..., M, K) } array\n        Unitary array(s). The first ``a.ndim - 2`` dimensions have the same\n        size as those of the input `a`. The size of the last two dimensions\n        depends on the value of `full_matrices`. Only returned when\n        `compute_uv` is True.\n    s : (..., K) array\n        Vector(s) with the singular values, within each vector sorted in\n        descending order. The first ``a.ndim - 2`` dimensions have the same\n        size as those of the input `a`.\n    vh : { (..., N, N), (..., K, N) } array\n        Unitary array(s). The first ``a.ndim - 2`` dimensions have the same\n        size as those of the input `a`. The size of the last two dimensions\n        depends on the value of `full_matrices`. Only returned when\n        `compute_uv` is True.\n\n    Raises\n    ------\n    LinAlgError\n        If SVD computation does not converge.\n\n    Notes\n    -----\n\n    .. versionchanged:: 1.8.0\n       Broadcasting rules apply, see the `numpy.linalg` documentation for\n       details.\n\n    The decomposition is performed using LAPACK routine ``_gesdd``.\n\n    SVD is usually described for the factorization of a 2D matrix :math:`A`.\n    The higher-dimensional case will be discussed below. In the 2D case, SVD is\n    written as :math:`A = U S V^H`, where :math:`A = a`, :math:`U= u`,\n    :math:`S= \\mathtt{np.diag}(s)` and :math:`V^H = vh`. The 1D array `s`\n    contains the singular values of `a` and `u` and `vh` are unitary. The rows\n    of `vh` are the eigenvectors of :math:`A^H A` and the columns of `u` are\n    the eigenvectors of :math:`A A^H`. In both cases the corresponding\n    (possibly non-zero) eigenvalues are given by ``s**2``.\n\n    If `a` has more than two dimensions, then broadcasting rules apply, as\n    explained in :ref:`routines.linalg-broadcasting`. This means that SVD is\n    working in "stacked" mode: it iterates over all indices of the first\n    ``a.ndim - 2`` dimensions and for each combination SVD is applied to the\n    last two indices. The matrix `a` can be reconstructed from the\n    decomposition with either ``(u * s[..., None, :]) @ vh`` or\n    ``u @ (s[..., None] * vh)``. (The ``@`` operator can be replaced by the\n    function ``np.matmul`` for python versions below 3.5.)\n\n    If `a` is a ``matrix`` object (as opposed to an ``ndarray``), then so are\n    all the return values.\n\n    Examples\n    --------\n    >>> a = np.random.randn(9, 6) + 1j*np.random.randn(9, 6)\n    >>> b = np.random.randn(2, 7, 8, 3) + 1j*np.random.randn(2, 7, 8, 3)\n\n    Reconstruction based on full SVD, 2D case:\n\n    >>> u, s, vh = np.linalg.svd(a, full_matrices=True)\n    >>> u.shape, s.shape, vh.shape\n    ((9, 9), (6,), (6, 6))\n    >>> np.allclose(a, np.dot(u[:, :6] * s, vh))\n    True\n    >>> smat = np.zeros((9, 6), dtype=complex)\n    >>> smat[:6, :6] = np.diag(s)\n    >>> np.allclose(a, np.dot(u, np.dot(smat, vh)))\n    True\n\n    Reconstruction based on reduced SVD, 2D case:\n\n    >>> u, s, vh = np.linalg.svd(a, full_matrices=False)\n    >>> u.shape, s.shape, vh.shape\n    ((9, 6), (6,), (6, 6))\n    >>> np.allclose(a, np.dot(u * s, vh))\n    True\n    >>> smat = np.diag(s)\n    >>> np.allclose(a, np.dot(u, np.dot(smat, vh)))\n    True\n\n    Reconstruction based on full SVD, 4D case:\n\n    >>> u, s, vh = np.linalg.svd(b, full_matrices=True)\n    >>> u.shape, s.shape, vh.shape\n    ((2, 7, 8, 8), (2, 7, 3), (2, 7, 3, 3))\n    >>> np.allclose(b, np.matmul(u[..., :3] * s[..., None, :], vh))\n    True\n    >>> np.allclose(b, np.matmul(u[..., :3], s[..., None] * vh))\n    True\n\n    Reconstruction based on reduced SVD, 4D case:\n\n    >>> u, s, vh = np.linalg.svd(b, full_matrices=False)\n    >>> u.shape, s.shape, vh.shape\n    ((2, 7, 8, 3), (2, 7, 3), (2, 7, 3, 3))\n    >>> np.allclose(b, np.matmul(u * s[..., None, :], vh))\n    True\n    >>> np.allclose(b, np.matmul(u, s[..., None] * vh))\n    True\n\n    '
    (a, wrap) = _makearray(a)
    if hermitian:
        if compute_uv:
            (s, u) = eigh(a)
            s = s[..., ::(- 1)]
            u = u[..., ::(- 1)]
            vt = transpose((u * sign(s)[..., None, :])).conjugate()
            s = abs(s)
            return (wrap(u), s, wrap(vt))
        else:
            s = eigvalsh(a)
            s = s[..., ::(- 1)]
            s = abs(s)
            return s
    _assert_stacked_2d(a)
    (t, result_t) = _commonType(a)
    extobj = get_linalg_error_extobj(_raise_linalgerror_svd_nonconvergence)
    (m, n) = a.shape[(- 2):]
    if compute_uv:
        if full_matrices:
            if (m < n):
                gufunc = _umath_linalg.svd_m_f
            else:
                gufunc = _umath_linalg.svd_n_f
        elif (m < n):
            gufunc = _umath_linalg.svd_m_s
        else:
            gufunc = _umath_linalg.svd_n_s
        signature = ('D->DdD' if isComplexType(t) else 'd->ddd')
        (u, s, vh) = gufunc(a, signature=signature, extobj=extobj)
        u = u.astype(result_t, copy=False)
        s = s.astype(_realType(result_t), copy=False)
        vh = vh.astype(result_t, copy=False)
        return (wrap(u), s, wrap(vh))
    else:
        if (m < n):
            gufunc = _umath_linalg.svd_m
        else:
            gufunc = _umath_linalg.svd_n
        signature = ('D->d' if isComplexType(t) else 'd->d')
        s = gufunc(a, signature=signature, extobj=extobj)
        s = s.astype(_realType(result_t), copy=False)
        return s