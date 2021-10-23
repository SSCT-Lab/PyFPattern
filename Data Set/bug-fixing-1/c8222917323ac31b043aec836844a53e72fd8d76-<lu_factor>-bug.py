

def lu_factor(a, overwrite_a=False, check_finite=True):
    "\n    Compute pivoted LU decomposition of a matrix.\n\n    The decomposition is::\n\n        A = P L U\n\n    where P is a permutation matrix, L lower triangular with unit\n    diagonal elements, and U upper triangular.\n\n    Parameters\n    ----------\n    a : (M, M) array_like\n        Matrix to decompose\n    overwrite_a : bool, optional\n        Whether to overwrite data in A (may increase performance)\n    check_finite : bool, optional\n        Whether to check that the input matrix contains only finite numbers.\n        Disabling may give a performance gain, but may result in problems\n        (crashes, non-termination) if the inputs do contain infinities or NaNs.\n\n    Returns\n    -------\n    lu : (N, N) ndarray\n        Matrix containing U in its upper triangle, and L in its lower triangle.\n        The unit diagonal elements of L are not stored.\n    piv : (N,) ndarray\n        Pivot indices representing the permutation matrix P:\n        row i of matrix was interchanged with row piv[i].\n\n    See also\n    --------\n    lu_solve : solve an equation system using the LU factorization of a matrix\n\n    Notes\n    -----\n    This is a wrapper to the ``*GETRF`` routines from LAPACK.\n\n    Examples\n    --------\n    >>> from scipy.linalg import lu_factor\n    >>> from numpy import tril, triu, allclose, zeros, eye\n    >>> A = np.array([[2, 5, 8, 7], [5, 2, 2, 8], [7, 5, 6, 6], [5, 4, 4, 8]])\n    >>> lu, piv = lu_factor(A)\n    >>> piv\n    array([2, 2, 3, 3], dtype=int32)\n    \n    Convert LAPACK's ``piv`` array to NumPy index and test the permutation \n    \n    >>> piv_py = [2, 0, 3, 1]\n    >>> L, U = np.tril(lu, k=-1) + np.eye(4), np.triu(lu)\n    >>> np.allclose(A[piv_py] - L @ U, np.zeros((4, 4)))\n    True\n    "
    if check_finite:
        a1 = asarray_chkfinite(a)
    else:
        a1 = asarray(a)
    if ((len(a1.shape) != 2) or (a1.shape[0] != a1.shape[1])):
        raise ValueError('expected square matrix')
    overwrite_a = (overwrite_a or _datacopied(a1, a))
    (getrf,) = get_lapack_funcs(('getrf',), (a1,))
    (lu, piv, info) = getrf(a1, overwrite_a=overwrite_a)
    if (info < 0):
        raise ValueError(('illegal value in %d-th argument of internal getrf (lu_factor)' % (- info)))
    if (info > 0):
        warn(('Diagonal number %d is exactly zero. Singular matrix.' % info), LinAlgWarning, stacklevel=2)
    return (lu, piv)
