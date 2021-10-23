

def eigs(A, k=6, M=None, sigma=None, which='LM', v0=None, ncv=None, maxiter=None, tol=0, return_eigenvectors=True, Minv=None, OPinv=None, OPpart=None):
    "\n    Find k eigenvalues and eigenvectors of the square matrix A.\n\n    Solves ``A * x[i] = w[i] * x[i]``, the standard eigenvalue problem\n    for w[i] eigenvalues with corresponding eigenvectors x[i].\n\n    If M is specified, solves ``A * x[i] = w[i] * M * x[i]``, the\n    generalized eigenvalue problem for w[i] eigenvalues\n    with corresponding eigenvectors x[i]\n\n    Parameters\n    ----------\n    A : ndarray, sparse matrix or LinearOperator\n        An array, sparse matrix, or LinearOperator representing\n        the operation ``A * x``, where A is a real or complex square matrix.\n    k : int, optional\n        The number of eigenvalues and eigenvectors desired.\n        `k` must be smaller than N-1. It is not possible to compute all\n        eigenvectors of a matrix.\n    M : ndarray, sparse matrix or LinearOperator, optional\n        An array, sparse matrix, or LinearOperator representing\n        the operation M*x for the generalized eigenvalue problem\n\n            A * x = w * M * x.\n\n        M must represent a real, symmetric matrix if A is real, and must\n        represent a complex, hermitian matrix if A is complex. For best\n        results, the data type of M should be the same as that of A.\n        Additionally:\n\n            If `sigma` is None, M is positive definite\n\n            If sigma is specified, M is positive semi-definite\n\n        If sigma is None, eigs requires an operator to compute the solution\n        of the linear equation ``M * x = b``.  This is done internally via a\n        (sparse) LU decomposition for an explicit matrix M, or via an\n        iterative solver for a general linear operator.  Alternatively,\n        the user can supply the matrix or operator Minv, which gives\n        ``x = Minv * b = M^-1 * b``.\n    sigma : real or complex, optional\n        Find eigenvalues near sigma using shift-invert mode.  This requires\n        an operator to compute the solution of the linear system\n        ``[A - sigma * M] * x = b``, where M is the identity matrix if\n        unspecified. This is computed internally via a (sparse) LU\n        decomposition for explicit matrices A & M, or via an iterative\n        solver if either A or M is a general linear operator.\n        Alternatively, the user can supply the matrix or operator OPinv,\n        which gives ``x = OPinv * b = [A - sigma * M]^-1 * b``.\n        For a real matrix A, shift-invert can either be done in imaginary\n        mode or real mode, specified by the parameter OPpart ('r' or 'i').\n        Note that when sigma is specified, the keyword 'which' (below)\n        refers to the shifted eigenvalues ``w'[i]`` where:\n\n            If A is real and OPpart == 'r' (default),\n              ``w'[i] = 1/2 * [1/(w[i]-sigma) + 1/(w[i]-conj(sigma))]``.\n\n            If A is real and OPpart == 'i',\n              ``w'[i] = 1/2i * [1/(w[i]-sigma) - 1/(w[i]-conj(sigma))]``.\n\n            If A is complex, ``w'[i] = 1/(w[i]-sigma)``.\n\n    v0 : ndarray, optional\n        Starting vector for iteration.\n        Default: random\n    ncv : int, optional\n        The number of Lanczos vectors generated\n        `ncv` must be greater than `k`; it is recommended that ``ncv > 2*k``.\n        Default: ``min(n, max(2*k + 1, 20))``\n    which : str, ['LM' | 'SM' | 'LR' | 'SR' | 'LI' | 'SI'], optional\n        Which `k` eigenvectors and eigenvalues to find:\n\n            'LM' : largest magnitude\n\n            'SM' : smallest magnitude\n\n            'LR' : largest real part\n\n            'SR' : smallest real part\n\n            'LI' : largest imaginary part\n\n            'SI' : smallest imaginary part\n\n        When sigma != None, 'which' refers to the shifted eigenvalues w'[i]\n        (see discussion in 'sigma', above).  ARPACK is generally better\n        at finding large values than small values.  If small eigenvalues are\n        desired, consider using shift-invert mode for better performance.\n    maxiter : int, optional\n        Maximum number of Arnoldi update iterations allowed\n        Default: ``n*10``\n    tol : float, optional\n        Relative accuracy for eigenvalues (stopping criterion)\n        The default value of 0 implies machine precision.\n    return_eigenvectors : bool, optional\n        Return eigenvectors (True) in addition to eigenvalues\n    Minv : ndarray, sparse matrix or LinearOperator, optional\n        See notes in M, above.\n    OPinv : ndarray, sparse matrix or LinearOperator, optional\n        See notes in sigma, above.\n    OPpart : {'r' or 'i'}, optional\n        See notes in sigma, above\n\n    Returns\n    -------\n    w : ndarray\n        Array of k eigenvalues.\n    v : ndarray\n        An array of `k` eigenvectors.\n        ``v[:, i]`` is the eigenvector corresponding to the eigenvalue w[i].\n\n    Raises\n    ------\n    ArpackNoConvergence\n        When the requested convergence is not obtained.\n        The currently converged eigenvalues and eigenvectors can be found\n        as ``eigenvalues`` and ``eigenvectors`` attributes of the exception\n        object.\n\n    See Also\n    --------\n    eigsh : eigenvalues and eigenvectors for symmetric matrix A\n    svds : singular value decomposition for a matrix A\n\n    Notes\n    -----\n    This function is a wrapper to the ARPACK [1]_ SNEUPD, DNEUPD, CNEUPD,\n    ZNEUPD, functions which use the Implicitly Restarted Arnoldi Method to\n    find the eigenvalues and eigenvectors [2]_.\n\n    References\n    ----------\n    .. [1] ARPACK Software, http://www.caam.rice.edu/software/ARPACK/\n    .. [2] R. B. Lehoucq, D. C. Sorensen, and C. Yang,  ARPACK USERS GUIDE:\n       Solution of Large Scale Eigenvalue Problems by Implicitly Restarted\n       Arnoldi Methods. SIAM, Philadelphia, PA, 1998.\n\n    Examples\n    --------\n    Find 6 eigenvectors of the identity matrix:\n\n    >>> from scipy.sparse.linalg import eigs\n    >>> id = np.eye(13)\n    >>> vals, vecs = eigs(id, k=6)\n    >>> vals\n    array([ 1.+0.j,  1.+0.j,  1.+0.j,  1.+0.j,  1.+0.j,  1.+0.j])\n    >>> vecs.shape\n    (13, 6)\n\n    "
    if (A.shape[0] != A.shape[1]):
        raise ValueError(('expected square matrix (shape=%s)' % (A.shape,)))
    if (M is not None):
        if (M.shape != A.shape):
            raise ValueError(('wrong M dimensions %s, should be %s' % (M.shape, A.shape)))
        if (np.dtype(M.dtype).char.lower() != np.dtype(A.dtype).char.lower()):
            warnings.warn('M does not have the same type precision as A. This may adversely affect ARPACK convergence')
    n = A.shape[0]
    if (k <= 0):
        raise ValueError(('k=%d must be greater than 0.' % k))
    if (k >= (n - 1)):
        warnings.warn('k >= N - 1 for N * N square matrix. Attempting to use scipy.linalg.eig instead.', RuntimeWarning)
        if issparse(A):
            raise TypeError('Cannot use scipy.linalg.eig for sparse A with k >= N - 1. Use scipy.linalg.eig(A.toarray()) or reduce k.')
        if isinstance(A, LinearOperator):
            raise TypeError('Cannot use scipy.linalg.eig for LinearOperator A with k >= N - 1.')
        if isinstance(M, LinearOperator):
            raise TypeError('Cannot use scipy.linalg.eig for LinearOperator M with k >= N - 1.')
        return eig(A, b=M, right=return_eigenvectors)
    if (sigma is None):
        matvec = _aslinearoperator_with_dtype(A).matvec
        if (OPinv is not None):
            raise ValueError('OPinv should not be specified with sigma = None.')
        if (OPpart is not None):
            raise ValueError('OPpart should not be specified with sigma = None or complex A')
        if (M is None):
            mode = 1
            M_matvec = None
            Minv_matvec = None
            if (Minv is not None):
                raise ValueError('Minv should not be specified with M = None.')
        else:
            mode = 2
            if (Minv is None):
                Minv_matvec = get_inv_matvec(M, symmetric=True, tol=tol)
            else:
                Minv = _aslinearoperator_with_dtype(Minv)
                Minv_matvec = Minv.matvec
            M_matvec = _aslinearoperator_with_dtype(M).matvec
    else:
        if np.issubdtype(A.dtype, np.complexfloating):
            if (OPpart is not None):
                raise ValueError('OPpart should not be specified with sigma=None or complex A')
            mode = 3
        elif ((OPpart is None) or (OPpart.lower() == 'r')):
            mode = 3
        elif (OPpart.lower() == 'i'):
            if (np.imag(sigma) == 0):
                raise ValueError("OPpart cannot be 'i' if sigma is real")
            mode = 4
        else:
            raise ValueError("OPpart must be one of ('r','i')")
        matvec = _aslinearoperator_with_dtype(A).matvec
        if (Minv is not None):
            raise ValueError('Minv should not be specified when sigma is')
        if (OPinv is None):
            Minv_matvec = get_OPinv_matvec(A, M, sigma, symmetric=False, tol=tol)
        else:
            OPinv = _aslinearoperator_with_dtype(OPinv)
            Minv_matvec = OPinv.matvec
        if (M is None):
            M_matvec = None
        else:
            M_matvec = _aslinearoperator_with_dtype(M).matvec
    params = _UnsymmetricArpackParams(n, k, A.dtype.char, matvec, mode, M_matvec, Minv_matvec, sigma, ncv, v0, maxiter, which, tol)
    with _ARPACK_LOCK:
        while (not params.converged):
            params.iterate()
        return params.extract(return_eigenvectors)
