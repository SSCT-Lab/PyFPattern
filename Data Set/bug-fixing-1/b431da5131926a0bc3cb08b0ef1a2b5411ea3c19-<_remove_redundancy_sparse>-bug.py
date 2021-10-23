

def _remove_redundancy_sparse(A, rhs):
    '\n    Eliminates redundant equations from system of equations defined by Ax = b\n    and identifies infeasibilities.\n\n    Parameters\n    ----------\n    A : 2-D sparse matrix\n        An matrix representing the left-hand side of a system of equations\n    rhs : 1-D array\n        An array representing the right-hand side of a system of equations\n\n    Returns\n    -------\n    A : 2-D sparse matrix\n        A matrix representing the left-hand side of a system of equations\n    rhs : 1-D array\n        An array representing the right-hand side of a system of equations\n    status: int\n        An integer indicating the status of the system\n        0: No infeasibility identified\n        2: Trivially infeasible\n    message : str\n        A string descriptor of the exit status of the optimization.\n\n    References\n    ----------\n    .. [2] Andersen, Erling D. "Finding all linearly dependent rows in\n           large-scale linear programming." Optimization Methods and Software\n           6.3 (1995): 219-227.\n\n    '
    tolapiv = 1e-08
    tolprimal = 1e-08
    status = 0
    message = ''
    inconsistent = 'There is a linear combination of rows of A_eq that results in zero, suggesting a redundant constraint. However the same linear combination of b_eq is nonzero, suggesting that the constraints conflict and the problem is infeasible.'
    (A, rhs, status, message) = _remove_zero_rows(A, rhs)
    if (status != 0):
        return (A, rhs, status, message)
    (m, n) = A.shape
    v = list(range(m))
    b = list(v)
    k = set(range(m, (m + n)))
    d = []
    A_orig = A
    A = scipy.sparse.hstack((scipy.sparse.eye(m), A)).tocsc()
    e = np.zeros(m)
    for i in v:
        B = A[:, b]
        e[i] = 1
        if (i > 0):
            e[(i - 1)] = 0
        pi = scipy.sparse.linalg.spsolve(B.transpose(), e).reshape((- 1), 1)
        js = list((k - set(b)))
        c = abs(A[:, js].transpose().dot(pi))
        if (c > tolapiv).any():
            j = js[np.argmax(c)]
            b[i] = j
        else:
            bibar = pi.T.dot(rhs.reshape((- 1), 1))
            bnorm = np.linalg.norm(rhs)
            if ((abs(bibar) / (1 + bnorm)) > tolprimal):
                status = 2
                message = inconsistent
                return (A_orig, rhs, status, message)
            else:
                d.append(i)
    keep = set(range(m))
    keep = list((keep - set(d)))
    return (A_orig[keep, :], rhs[keep], status, message)
