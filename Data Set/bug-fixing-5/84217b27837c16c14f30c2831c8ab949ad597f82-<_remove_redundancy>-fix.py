def _remove_redundancy(A, b):
    '\n    Eliminates redundant equations from system of equations defined by Ax = b\n    and identifies infeasibilities.\n\n    Parameters\n    ----------\n    A : 2-D array\n        An array representing the left-hand side of a system of equations\n    b : 1-D array\n        An array representing the right-hand side of a system of equations\n\n    Returns\n    -------\n    A : 2-D array\n        An array representing the left-hand side of a system of equations\n    b : 1-D array\n        An array representing the right-hand side of a system of equations\n    status: int\n        An integer indicating the status of the system\n        0: No infeasibility identified\n        2: Trivially infeasible\n    message : str\n        A string descriptor of the exit status of the optimization.\n\n    References\n    ----------\n    .. [2] Andersen, Erling D. "Finding all linearly dependent rows in\n           large-scale linear programming." Optimization Methods and Software\n           6.3 (1995): 219-227.\n\n    '
    (A, b, status, message) = _remove_zero_rows(A, b)
    if (status != 0):
        return (A, b, status, message)
    (U, s, Vh) = svd(A)
    eps = np.finfo(float).eps
    tol = ((s.max() * max(A.shape)) * eps)
    (m, n) = A.shape
    s_min = (s[(- 1)] if (m <= n) else 0)
    while (abs(s_min) < tol):
        v = U[:, (- 1)]
        eligibleRows = (np.abs(v) > (tol * 10000000.0))
        if ((not np.any(eligibleRows)) or np.any((np.abs(v.dot(A)) > tol))):
            status = 4
            message = 'Due to numerical issues, redundant equality constraints could not be removed automatically. Try providing your constraint matrices as sparse matrices to activate sparse presolve, try turning off redundancy removal, or try turning off presolve altogether.'
            break
        if np.any((np.abs(v.dot(b)) > (tol * 10))):
            status = 2
            message = 'There is a linear combination of rows of A_eq that results in zero, suggesting a redundant constraint. However the same linear combination of b_eq is nonzero, suggesting that the constraints conflict and the problem is infeasible.'
            break
        i_remove = _get_densest(A, eligibleRows)
        A = np.delete(A, i_remove, axis=0)
        b = np.delete(b, i_remove)
        (U, s, Vh) = svd(A)
        (m, n) = A.shape
        s_min = (s[(- 1)] if (m <= n) else 0)
    return (A, b, status, message)