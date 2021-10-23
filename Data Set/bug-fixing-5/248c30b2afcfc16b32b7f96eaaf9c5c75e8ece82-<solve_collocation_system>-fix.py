def solve_collocation_system(fun, t, y, h, Z0, scale, tol, LU_real, LU_complex, solve_lu):
    'Solve the collocation system.\n\n    Parameters\n    ----------\n    fun : callable\n        Right-hand side of the system.\n    t : float\n        Current time.\n    y : ndarray, shape (n,)\n        Current state.\n    h : float\n        Step to try.\n    Z0 : ndarray, shape (3, n)\n        Initial guess for the solution. It determines new values of `y` at\n        ``t + h * C`` as ``y + Z0``, where ``C`` is the Radau method constants.\n    scale : float\n        Problem tolerance scale, i.e. ``rtol * abs(y) + atol``.\n    tol : float\n        Tolerance to which solve the system. This value is compared with\n        the normalized by `scale` error.\n    LU_real, LU_complex\n        LU decompositions of the system Jacobians.\n    solve_lu : callable\n        Callable which solves a linear system given a LU decomposition. The\n        signature is ``solve_lu(LU, b)``.\n\n    Returns\n    -------\n    converged : bool\n        Whether iterations converged.\n    n_iter : int\n        Number of completed iterations.\n    Z : ndarray, shape (3, n)\n        Found solution.\n    rate : float\n        The rate of convergence.\n    '
    n = y.shape[0]
    M_real = (MU_REAL / h)
    M_complex = (MU_COMPLEX / h)
    W = TI.dot(Z0)
    Z = Z0
    F = np.empty((3, n))
    ch = (h * C)
    dW_norm_old = None
    dW = np.empty_like(W)
    converged = False
    rate = None
    for k in range(NEWTON_MAXITER):
        for i in range(3):
            F[i] = fun((t + ch[i]), (y + Z[i]))
        if (not np.all(np.isfinite(F))):
            break
        f_real = (F.T.dot(TI_REAL) - (M_real * W[0]))
        f_complex = (F.T.dot(TI_COMPLEX) - (M_complex * (W[1] + (1j * W[2]))))
        dW_real = solve_lu(LU_real, f_real)
        dW_complex = solve_lu(LU_complex, f_complex)
        dW[0] = dW_real
        dW[1] = dW_complex.real
        dW[2] = dW_complex.imag
        dW_norm = norm((dW / scale))
        if (dW_norm_old is not None):
            rate = (dW_norm / dW_norm_old)
        if ((rate is not None) and ((rate >= 1) or ((((rate ** (NEWTON_MAXITER - k)) / (1 - rate)) * dW_norm) > tol))):
            break
        W += dW
        Z = T.dot(W)
        if ((dW_norm == 0) or ((rate is not None) and (((rate / (1 - rate)) * dW_norm) < tol))):
            converged = True
            break
        dW_norm_old = dW_norm
    return (converged, (k + 1), Z, rate)