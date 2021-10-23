@array_function_dispatch(_pinv_dispatcher)
def pinv(a, rcond=1e-15, hermitian=False):
    '\n    Compute the (Moore-Penrose) pseudo-inverse of a matrix.\n\n    Calculate the generalized inverse of a matrix using its\n    singular-value decomposition (SVD) and including all\n    *large* singular values.\n\n    .. versionchanged:: 1.14\n       Can now operate on stacks of matrices\n\n    Parameters\n    ----------\n    a : (..., M, N) array_like\n        Matrix or stack of matrices to be pseudo-inverted.\n    rcond : (...) array_like of float\n        Cutoff for small singular values.\n        Singular values less than or equal to\n        ``rcond * largest_singular_value`` are set to zero.\n        Broadcasts against the stack of matrices.\n    hermitian : bool, optional\n        If True, `a` is assumed to be Hermitian (symmetric if real-valued),\n        enabling a more efficient method for finding singular values.\n        Defaults to False.\n\n        .. versionadded:: 1.17.0\n\n    Returns\n    -------\n    B : (..., N, M) ndarray\n        The pseudo-inverse of `a`. If `a` is a `matrix` instance, then so\n        is `B`.\n\n    Raises\n    ------\n    LinAlgError\n        If the SVD computation does not converge.\n\n    Notes\n    -----\n    The pseudo-inverse of a matrix A, denoted :math:`A^+`, is\n    defined as: "the matrix that \'solves\' [the least-squares problem]\n    :math:`Ax = b`," i.e., if :math:`\\bar{x}` is said solution, then\n    :math:`A^+` is that matrix such that :math:`\\bar{x} = A^+b`.\n\n    It can be shown that if :math:`Q_1 \\Sigma Q_2^T = A` is the singular\n    value decomposition of A, then\n    :math:`A^+ = Q_2 \\Sigma^+ Q_1^T`, where :math:`Q_{1,2}` are\n    orthogonal matrices, :math:`\\Sigma` is a diagonal matrix consisting\n    of A\'s so-called singular values, (followed, typically, by\n    zeros), and then :math:`\\Sigma^+` is simply the diagonal matrix\n    consisting of the reciprocals of A\'s singular values\n    (again, followed by zeros). [1]_\n\n    References\n    ----------\n    .. [1] G. Strang, *Linear Algebra and Its Applications*, 2nd Ed., Orlando,\n           FL, Academic Press, Inc., 1980, pp. 139-142.\n\n    Examples\n    --------\n    The following example checks that ``a * a+ * a == a`` and\n    ``a+ * a * a+ == a+``:\n\n    >>> a = np.random.randn(9, 6)\n    >>> B = np.linalg.pinv(a)\n    >>> np.allclose(a, np.dot(a, np.dot(B, a)))\n    True\n    >>> np.allclose(B, np.dot(B, np.dot(a, B)))\n    True\n\n    '
    (a, wrap) = _makearray(a)
    rcond = asarray(rcond)
    if _is_empty_2d(a):
        (m, n) = a.shape[(- 2):]
        res = empty((a.shape[:(- 2)] + (n, m)), dtype=a.dtype)
        return wrap(res)
    a = a.conjugate()
    (u, s, vt) = svd(a, full_matrices=False, hermitian=hermitian)
    cutoff = (rcond[(..., newaxis)] * amax(s, axis=(- 1), keepdims=True))
    large = (s > cutoff)
    s = divide(1, s, where=large, out=s)
    s[(~ large)] = 0
    res = matmul(transpose(vt), multiply(s[(..., newaxis)], transpose(u)))
    return wrap(res)