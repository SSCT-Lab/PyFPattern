

def _minimize_lbfgsb(fun, x0, args=(), jac=None, bounds=None, disp=None, maxcor=10, ftol=2.220446049250313e-09, gtol=1e-05, eps=1e-08, maxfun=15000, maxiter=15000, iprint=(- 1), callback=None, maxls=20, **unknown_options):
    '\n    Minimize a scalar function of one or more variables using the L-BFGS-B\n    algorithm.\n\n    Options\n    -------\n    disp : None or int\n        If `disp is None` (the default), then the supplied version of `iprint`\n        is used. If `disp is not None`, then it overrides the supplied version\n        of `iprint` with the behaviour you outlined.\n    maxcor : int\n        The maximum number of variable metric corrections used to\n        define the limited memory matrix. (The limited memory BFGS\n        method does not store the full hessian but uses this many terms\n        in an approximation to it.)\n    ftol : float\n        The iteration stops when ``(f^k -\n        f^{k+1})/max{|f^k|,|f^{k+1}|,1} <= ftol``.\n    gtol : float\n        The iteration will stop when ``max{|proj g_i | i = 1, ..., n}\n        <= gtol`` where ``pg_i`` is the i-th component of the\n        projected gradient.\n    eps : float\n        Step size used for numerical approximation of the jacobian.\n    maxfun : int\n        Maximum number of function evaluations.\n    maxiter : int\n        Maximum number of iterations.\n    maxls : int, optional\n        Maximum number of line search steps (per iteration). Default is 20.\n\n    Notes\n    -----\n    The option `ftol` is exposed via the `scipy.optimize.minimize` interface,\n    but calling `scipy.optimize.fmin_l_bfgs_b` directly exposes `factr`. The\n    relationship between the two is ``ftol = factr * numpy.finfo(float).eps``.\n    I.e., `factr` multiplies the default machine floating-point precision to\n    arrive at `ftol`.\n\n    '
    _check_unknown_options(unknown_options)
    m = maxcor
    epsilon = eps
    pgtol = gtol
    factr = (ftol / np.finfo(float).eps)
    x0 = asarray(x0).ravel()
    (n,) = x0.shape
    if (bounds is None):
        bounds = ([(None, None)] * n)
    if (len(bounds) != n):
        raise ValueError('length of x0 != length of bounds')
    bounds = [((None if (l == (- np.inf)) else l), (None if (u == np.inf) else u)) for (l, u) in bounds]
    if (disp is not None):
        if (disp == 0):
            iprint = (- 1)
        else:
            iprint = disp
    (n_function_evals, fun) = wrap_function(fun, ())
    if (jac is None):

        def func_and_grad(x):
            f = fun(x, *args)
            g = _approx_fprime_helper(x, fun, epsilon, args=args, f0=f)
            return (f, g)
    else:

        def func_and_grad(x):
            f = fun(x, *args)
            g = jac(x, *args)
            return (f, g)
    nbd = zeros(n, int32)
    low_bnd = zeros(n, float64)
    upper_bnd = zeros(n, float64)
    bounds_map = {
        (None, None): 0,
        (1, None): 1,
        (1, 1): 2,
        (None, 1): 3,
    }
    for i in range(0, n):
        (l, u) = bounds[i]
        if (l is not None):
            low_bnd[i] = l
            l = 1
        if (u is not None):
            upper_bnd[i] = u
            u = 1
        nbd[i] = bounds_map[(l, u)]
    if (not (maxls > 0)):
        raise ValueError('maxls must be positive.')
    x = array(x0, float64)
    f = array(0.0, float64)
    g = zeros((n,), float64)
    wa = zeros((((((2 * m) * n) + (5 * n)) + ((11 * m) * m)) + (8 * m)), float64)
    iwa = zeros((3 * n), int32)
    task = zeros(1, 'S60')
    csave = zeros(1, 'S60')
    lsave = zeros(4, int32)
    isave = zeros(44, int32)
    dsave = zeros(29, float64)
    task[:] = 'START'
    n_iterations = 0
    while 1:
        _lbfgsb.setulb(m, x, low_bnd, upper_bnd, nbd, f, g, factr, pgtol, wa, iwa, task, iprint, csave, lsave, isave, dsave, maxls)
        task_str = task.tostring()
        if task_str.startswith(b'FG'):
            (f, g) = func_and_grad(x)
        elif task_str.startswith(b'NEW_X'):
            n_iterations += 1
            if (callback is not None):
                callback(np.copy(x))
            if (n_iterations >= maxiter):
                task[:] = 'STOP: TOTAL NO. of ITERATIONS REACHED LIMIT'
            elif (n_function_evals[0] > maxfun):
                task[:] = 'STOP: TOTAL NO. of f AND g EVALUATIONS EXCEEDS LIMIT'
        else:
            break
    task_str = task.tostring().strip(b'\x00').strip()
    if task_str.startswith(b'CONV'):
        warnflag = 0
    elif ((n_function_evals[0] > maxfun) or (n_iterations >= maxiter)):
        warnflag = 1
    else:
        warnflag = 2
    s = wa[0:(m * n)].reshape(m, n)
    y = wa[(m * n):((2 * m) * n)].reshape(m, n)
    n_bfgs_updates = isave[30]
    n_corrs = min(n_bfgs_updates, maxcor)
    hess_inv = LbfgsInvHessProduct(s[:n_corrs], y[:n_corrs])
    return OptimizeResult(fun=f, jac=g, nfev=n_function_evals[0], nit=n_iterations, status=warnflag, message=task_str, x=x, success=(warnflag == 0), hess_inv=hess_inv)
