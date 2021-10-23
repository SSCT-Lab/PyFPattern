def nnls(A, b):
    '\n    Solve ``argmin_x || Ax - b ||_2`` for ``x>=0``. This is a wrapper\n    for a FORTAN non-negative least squares solver.\n\n    Parameters\n    ----------\n    A : ndarray\n        Matrix ``A`` as shown above.\n    b : ndarray\n        Right-hand side vector.\n\n    Returns\n    -------\n    x : ndarray\n        Solution vector.\n    rnorm : float\n        The residual, ``|| Ax-b ||_2``.\n\n    Notes\n    -----\n    The FORTRAN code was published in the book below. The algorithm\n    is an active set method. It solves the KKT (Karush-Kuhn-Tucker)\n    conditions for the non-negative least squares problem.\n\n    References\n    ----------\n    Lawson C., Hanson R.J., (1987) Solving Least Squares Problems, SIAM\n\n    '
    (A, b) = map(asarray_chkfinite, (A, b))
    if (len(A.shape) != 2):
        raise ValueError('expected matrix')
    if (len(b.shape) != 1):
        raise ValueError('expected vector')
    (m, n) = A.shape
    if (m != b.shape[0]):
        raise ValueError('incompatible dimensions')
    w = zeros((n,), dtype=double)
    zz = zeros((m,), dtype=double)
    index = zeros((n,), dtype=int)
    (x, rnorm, mode) = _nnls.nnls(A, m, n, b, w, zz, index)
    if (mode != 1):
        raise RuntimeError('too many iterations')
    return (x, rnorm)