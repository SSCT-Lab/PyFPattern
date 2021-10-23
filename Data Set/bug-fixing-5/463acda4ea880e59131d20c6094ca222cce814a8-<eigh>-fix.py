@array_function_dispatch(_eigvalsh_dispatcher)
def eigh(a, UPLO='L'):
    "\n    Return the eigenvalues and eigenvectors of a complex Hermitian\n    (conjugate symmetric) or a real symmetric matrix.\n\n    Returns two objects, a 1-D array containing the eigenvalues of `a`, and\n    a 2-D square array or matrix (depending on the input type) of the\n    corresponding eigenvectors (in columns).\n\n    Parameters\n    ----------\n    a : (..., M, M) array\n        Hermitian or real symmetric matrices whose eigenvalues and\n        eigenvectors are to be computed.\n    UPLO : {'L', 'U'}, optional\n        Specifies whether the calculation is done with the lower triangular\n        part of `a` ('L', default) or the upper triangular part ('U').\n        Irrespective of this value only the real parts of the diagonal will\n        be considered in the computation to preserve the notion of a Hermitian\n        matrix. It therefore follows that the imaginary part of the diagonal\n        will always be treated as zero.\n\n    Returns\n    -------\n    w : (..., M) ndarray\n        The eigenvalues in ascending order, each repeated according to\n        its multiplicity.\n    v : {(..., M, M) ndarray, (..., M, M) matrix}\n        The column ``v[:, i]`` is the normalized eigenvector corresponding\n        to the eigenvalue ``w[i]``.  Will return a matrix object if `a` is\n        a matrix object.\n\n    Raises\n    ------\n    LinAlgError\n        If the eigenvalue computation does not converge.\n\n    See Also\n    --------\n    eigvalsh : eigenvalues of real symmetric or complex Hermitian\n               (conjugate symmetric) arrays.\n    eig : eigenvalues and right eigenvectors for non-symmetric arrays.\n    eigvals : eigenvalues of non-symmetric arrays.\n\n    Notes\n    -----\n\n    .. versionadded:: 1.8.0\n\n    Broadcasting rules apply, see the `numpy.linalg` documentation for\n    details.\n\n    The eigenvalues/eigenvectors are computed using LAPACK routines ``_syevd``,\n    ``_heevd``.\n\n    The eigenvalues of real symmetric or complex Hermitian matrices are\n    always real. [1]_ The array `v` of (column) eigenvectors is unitary\n    and `a`, `w`, and `v` satisfy the equations\n    ``dot(a, v[:, i]) = w[i] * v[:, i]``.\n\n    References\n    ----------\n    .. [1] G. Strang, *Linear Algebra and Its Applications*, 2nd Ed., Orlando,\n           FL, Academic Press, Inc., 1980, pg. 222.\n\n    Examples\n    --------\n    >>> from numpy import linalg as LA\n    >>> a = np.array([[1, -2j], [2j, 5]])\n    >>> a\n    array([[ 1.+0.j, -0.-2.j],\n           [ 0.+2.j,  5.+0.j]])\n    >>> w, v = LA.eigh(a)\n    >>> w; v\n    array([0.17157288, 5.82842712])\n    array([[-0.92387953+0.j        , -0.38268343+0.j        ], # may vary\n           [ 0.        +0.38268343j,  0.        -0.92387953j]])\n\n    >>> np.dot(a, v[:, 0]) - w[0] * v[:, 0] # verify 1st e-val/vec pair\n    array([5.55111512e-17+0.0000000e+00j, 0.00000000e+00+1.2490009e-16j])\n    >>> np.dot(a, v[:, 1]) - w[1] * v[:, 1] # verify 2nd e-val/vec pair\n    array([0.+0.j, 0.+0.j])\n\n    >>> A = np.matrix(a) # what happens if input is a matrix object\n    >>> A\n    matrix([[ 1.+0.j, -0.-2.j],\n            [ 0.+2.j,  5.+0.j]])\n    >>> w, v = LA.eigh(A)\n    >>> w; v\n    array([0.17157288, 5.82842712])\n    matrix([[-0.92387953+0.j        , -0.38268343+0.j        ], # may vary\n            [ 0.        +0.38268343j,  0.        -0.92387953j]])\n\n    >>> # demonstrate the treatment of the imaginary part of the diagonal\n    >>> a = np.array([[5+2j, 9-2j], [0+2j, 2-1j]])\n    >>> a\n    array([[5.+2.j, 9.-2.j],\n           [0.+2.j, 2.-1.j]])\n    >>> # with UPLO='L' this is numerically equivalent to using LA.eig() with:\n    >>> b = np.array([[5.+0.j, 0.-2.j], [0.+2.j, 2.-0.j]])\n    >>> b\n    array([[5.+0.j, 0.-2.j],\n           [0.+2.j, 2.+0.j]])\n    >>> wa, va = LA.eigh(a)\n    >>> wb, vb = LA.eig(b)\n    >>> wa; wb\n    array([1., 6.])\n    array([6.+0.j, 1.+0.j])\n    >>> va; vb\n    array([[-0.4472136 +0.j        , -0.89442719+0.j        ], # may vary\n           [ 0.        +0.89442719j,  0.        -0.4472136j ]])\n    array([[ 0.89442719+0.j       , -0.        +0.4472136j],\n           [-0.        +0.4472136j,  0.89442719+0.j       ]])\n    "
    UPLO = UPLO.upper()
    if (UPLO not in ('L', 'U')):
        raise ValueError("UPLO argument must be 'L' or 'U'")
    (a, wrap) = _makearray(a)
    _assert_stacked_2d(a)
    _assert_stacked_square(a)
    (t, result_t) = _commonType(a)
    extobj = get_linalg_error_extobj(_raise_linalgerror_eigenvalues_nonconvergence)
    if (UPLO == 'L'):
        gufunc = _umath_linalg.eigh_lo
    else:
        gufunc = _umath_linalg.eigh_up
    signature = ('D->dD' if isComplexType(t) else 'd->dd')
    (w, vt) = gufunc(a, signature=signature, extobj=extobj)
    w = w.astype(_realType(result_t), copy=False)
    vt = vt.astype(result_t, copy=False)
    return (w, wrap(vt))