@array_function_dispatch(_unary_dispatcher)
def eigvals(a):
    '\n    Compute the eigenvalues of a general matrix.\n\n    Main difference between `eigvals` and `eig`: the eigenvectors aren\'t\n    returned.\n\n    Parameters\n    ----------\n    a : (..., M, M) array_like\n        A complex- or real-valued matrix whose eigenvalues will be computed.\n\n    Returns\n    -------\n    w : (..., M,) ndarray\n        The eigenvalues, each repeated according to its multiplicity.\n        They are not necessarily ordered, nor are they necessarily\n        real for real matrices.\n\n    Raises\n    ------\n    LinAlgError\n        If the eigenvalue computation does not converge.\n\n    See Also\n    --------\n    eig : eigenvalues and right eigenvectors of general arrays\n    eigvalsh : eigenvalues of real symmetric or complex Hermitian\n               (conjugate symmetric) arrays.\n    eigh : eigenvalues and eigenvectors of real symmetric or complex\n           Hermitian (conjugate symmetric) arrays.\n\n    Notes\n    -----\n\n    .. versionadded:: 1.8.0\n\n    Broadcasting rules apply, see the `numpy.linalg` documentation for\n    details.\n\n    This is implemented using the _geev LAPACK routines which compute\n    the eigenvalues and eigenvectors of general square arrays.\n\n    Examples\n    --------\n    Illustration, using the fact that the eigenvalues of a diagonal matrix\n    are its diagonal elements, that multiplying a matrix on the left\n    by an orthogonal matrix, `Q`, and on the right by `Q.T` (the transpose\n    of `Q`), preserves the eigenvalues of the "middle" matrix.  In other words,\n    if `Q` is orthogonal, then ``Q * A * Q.T`` has the same eigenvalues as\n    ``A``:\n\n    >>> from numpy import linalg as LA\n    >>> x = np.random.random()\n    >>> Q = np.array([[np.cos(x), -np.sin(x)], [np.sin(x), np.cos(x)]])\n    >>> LA.norm(Q[0, :]), LA.norm(Q[1, :]), np.dot(Q[0, :],Q[1, :])\n    (1.0, 1.0, 0.0)\n\n    Now multiply a diagonal matrix by Q on one side and by Q.T on the other:\n\n    >>> D = np.diag((-1,1))\n    >>> LA.eigvals(D)\n    array([-1.,  1.])\n    >>> A = np.dot(Q, D)\n    >>> A = np.dot(A, Q.T)\n    >>> LA.eigvals(A)\n    array([ 1., -1.]) # random\n\n    '
    (a, wrap) = _makearray(a)
    _assertRankAtLeast2(a)
    _assertNdSquareness(a)
    _assertFinite(a)
    (t, result_t) = _commonType(a)
    extobj = get_linalg_error_extobj(_raise_linalgerror_eigenvalues_nonconvergence)
    signature = ('D->D' if isComplexType(t) else 'd->D')
    w = _umath_linalg.eigvals(a, signature=signature, extobj=extobj)
    if (not isComplexType(t)):
        if all((w.imag == 0)):
            w = w.real
            result_t = _realType(result_t)
        else:
            result_t = _complexType(result_t)
    return w.astype(result_t, copy=False)