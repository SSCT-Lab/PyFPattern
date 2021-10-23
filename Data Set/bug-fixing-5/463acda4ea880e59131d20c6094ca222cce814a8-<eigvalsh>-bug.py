@array_function_dispatch(_eigvalsh_dispatcher)
def eigvalsh(a, UPLO='L'):
    "\n    Compute the eigenvalues of a complex Hermitian or real symmetric matrix.\n\n    Main difference from eigh: the eigenvectors are not computed.\n\n    Parameters\n    ----------\n    a : (..., M, M) array_like\n        A complex- or real-valued matrix whose eigenvalues are to be\n        computed.\n    UPLO : {'L', 'U'}, optional\n        Specifies whether the calculation is done with the lower triangular\n        part of `a` ('L', default) or the upper triangular part ('U').\n        Irrespective of this value only the real parts of the diagonal will\n        be considered in the computation to preserve the notion of a Hermitian\n        matrix. It therefore follows that the imaginary part of the diagonal\n        will always be treated as zero.\n\n    Returns\n    -------\n    w : (..., M,) ndarray\n        The eigenvalues in ascending order, each repeated according to\n        its multiplicity.\n\n    Raises\n    ------\n    LinAlgError\n        If the eigenvalue computation does not converge.\n\n    See Also\n    --------\n    eigh : eigenvalues and eigenvectors of real symmetric or complex Hermitian\n           (conjugate symmetric) arrays.\n    eigvals : eigenvalues of general real or complex arrays.\n    eig : eigenvalues and right eigenvectors of general real or complex\n          arrays.\n\n    Notes\n    -----\n\n    .. versionadded:: 1.8.0\n\n    Broadcasting rules apply, see the `numpy.linalg` documentation for\n    details.\n\n    The eigenvalues are computed using LAPACK routines ``_syevd``, ``_heevd``.\n\n    Examples\n    --------\n    >>> from numpy import linalg as LA\n    >>> a = np.array([[1, -2j], [2j, 5]])\n    >>> LA.eigvalsh(a)\n    array([ 0.17157288,  5.82842712]) # may vary\n\n    >>> # demonstrate the treatment of the imaginary part of the diagonal\n    >>> a = np.array([[5+2j, 9-2j], [0+2j, 2-1j]])\n    >>> a\n    array([[5.+2.j, 9.-2.j],\n           [0.+2.j, 2.-1.j]])\n    >>> # with UPLO='L' this is numerically equivalent to using LA.eigvals()\n    >>> # with:\n    >>> b = np.array([[5.+0.j, 0.-2.j], [0.+2.j, 2.-0.j]])\n    >>> b\n    array([[5.+0.j, 0.-2.j],\n           [0.+2.j, 2.+0.j]])\n    >>> wa = LA.eigvalsh(a)\n    >>> wb = LA.eigvals(b)\n    >>> wa; wb\n    array([1., 6.])\n    array([6.+0.j, 1.+0.j])\n\n    "
    UPLO = UPLO.upper()
    if (UPLO not in ('L', 'U')):
        raise ValueError("UPLO argument must be 'L' or 'U'")
    extobj = get_linalg_error_extobj(_raise_linalgerror_eigenvalues_nonconvergence)
    if (UPLO == 'L'):
        gufunc = _umath_linalg.eigvalsh_lo
    else:
        gufunc = _umath_linalg.eigvalsh_up
    (a, wrap) = _makearray(a)
    _assertRankAtLeast2(a)
    _assertNdSquareness(a)
    (t, result_t) = _commonType(a)
    signature = ('D->d' if isComplexType(t) else 'd->d')
    w = gufunc(a, signature=signature, extobj=extobj)
    return w.astype(_realType(result_t), copy=False)