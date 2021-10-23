def _onenorm_matrix_power_nnm(A, p):
    '\n    Compute the 1-norm of a non-negative integer power of a non-negative matrix.\n\n    Parameters\n    ----------\n    A : a square ndarray or matrix or sparse matrix\n        Input matrix with non-negative entries.\n    p : non-negative integer\n        The power to which the matrix is to be raised.\n\n    Returns\n    -------\n    out : float\n        The 1-norm of the matrix power p of A.\n\n    '
    if ((int(p) != p) or (p < 0)):
        raise ValueError('expected non-negative integer p')
    p = int(p)
    if ((len(A.shape) != 2) or (A.shape[0] != A.shape[1])):
        raise ValueError('expected A to be like a square matrix')
    v = np.ones((A.shape[0], 1), dtype=float)
    M = A.T
    for i in range(p):
        v = M.dot(v)
    return np.max(v)