def fmin_l_bfgs_b(func, x0, fprime=None, args=(), approx_grad=0, bounds=None, m=10, factr=10000000.0, pgtol=1e-05, epsilon=1e-08, iprint=(- 1), maxfun=15000, maxiter=15000, disp=None, callback=None, maxls=20):
    "\n    Minimize a function func using the L-BFGS-B algorithm.\n\n    Parameters\n    ----------\n    func : callable f(x,*args)\n        Function to minimise.\n    x0 : ndarray\n        Initial guess.\n    fprime : callable fprime(x,*args), optional\n        The gradient of `func`.  If None, then `func` returns the function\n        value and the gradient (``f, g = func(x, *args)``), unless\n        `approx_grad` is True in which case `func` returns only ``f``.\n    args : sequence, optional\n        Arguments to pass to `func` and `fprime`.\n    approx_grad : bool, optional\n        Whether to approximate the gradient numerically (in which case\n        `func` returns only the function value).\n    bounds : list, optional\n        ``(min, max)`` pairs for each element in ``x``, defining\n        the bounds on that parameter. Use None or +-inf for one of ``min`` or\n        ``max`` when there is no bound in that direction.\n    m : int, optional\n        The maximum number of variable metric corrections\n        used to define the limited memory matrix. (The limited memory BFGS\n        method does not store the full hessian but uses this many terms in an\n        approximation to it.)\n    factr : float, optional\n        The iteration stops when\n        ``(f^k - f^{k+1})/max{|f^k|,|f^{k+1}|,1} <= factr * eps``,\n        where ``eps`` is the machine precision, which is automatically\n        generated by the code. Typical values for `factr` are: 1e12 for\n        low accuracy; 1e7 for moderate accuracy; 10.0 for extremely\n        high accuracy. See Notes for relationship to `ftol`, which is exposed\n        (instead of `factr`) by the `scipy.optimize.minimize` interface to\n        L-BFGS-B.\n    pgtol : float, optional\n        The iteration will stop when\n        ``max{|proj g_i | i = 1, ..., n} <= pgtol``\n        where ``pg_i`` is the i-th component of the projected gradient.\n    epsilon : float, optional\n        Step size used when `approx_grad` is True, for numerically\n        calculating the gradient\n    iprint : int, optional\n        Controls the frequency of output. ``iprint < 0`` means no output;\n        ``iprint = 0``    print only one line at the last iteration;\n        ``0 < iprint < 99`` print also f and ``|proj g|`` every iprint iterations;\n        ``iprint = 99``   print details of every iteration except n-vectors;\n        ``iprint = 100``  print also the changes of active set and final x;\n        ``iprint > 100``  print details of every iteration including x and g.\n    disp : int, optional\n        If zero, then no output.  If a positive number, then this over-rides\n        `iprint` (i.e., `iprint` gets the value of `disp`).\n    maxfun : int, optional\n        Maximum number of function evaluations.\n    maxiter : int, optional\n        Maximum number of iterations.\n    callback : callable, optional\n        Called after each iteration, as ``callback(xk)``, where ``xk`` is the\n        current parameter vector.\n    maxls : int, optional\n        Maximum number of line search steps (per iteration). Default is 20.\n\n    Returns\n    -------\n    x : array_like\n        Estimated position of the minimum.\n    f : float\n        Value of `func` at the minimum.\n    d : dict\n        Information dictionary.\n\n        * d['warnflag'] is\n\n          - 0 if converged,\n          - 1 if too many function evaluations or too many iterations,\n          - 2 if stopped for another reason, given in d['task']\n\n        * d['grad'] is the gradient at the minimum (should be 0 ish)\n        * d['funcalls'] is the number of function calls made.\n        * d['nit'] is the number of iterations.\n\n    See also\n    --------\n    minimize: Interface to minimization algorithms for multivariate\n        functions. See the 'L-BFGS-B' `method` in particular. Note that the\n        `ftol` option is made available via that interface, while `factr` is\n        provided via this interface, where `factr` is the factor multiplying\n        the default machine floating-point precision to arrive at `ftol`:\n        ``ftol = factr * numpy.finfo(float).eps``.\n\n    Notes\n    -----\n    License of L-BFGS-B (FORTRAN code):\n\n    The version included here (in fortran code) is 3.0\n    (released April 25, 2011).  It was written by Ciyou Zhu, Richard Byrd,\n    and Jorge Nocedal <nocedal@ece.nwu.edu>. It carries the following\n    condition for use:\n\n    This software is freely available, but we expect that all publications\n    describing work using this software, or all commercial products using it,\n    quote at least one of the references given below. This software is released\n    under the BSD License.\n\n    References\n    ----------\n    * R. H. Byrd, P. Lu and J. Nocedal. A Limited Memory Algorithm for Bound\n      Constrained Optimization, (1995), SIAM Journal on Scientific and\n      Statistical Computing, 16, 5, pp. 1190-1208.\n    * C. Zhu, R. H. Byrd and J. Nocedal. L-BFGS-B: Algorithm 778: L-BFGS-B,\n      FORTRAN routines for large scale bound constrained optimization (1997),\n      ACM Transactions on Mathematical Software, 23, 4, pp. 550 - 560.\n    * J.L. Morales and J. Nocedal. L-BFGS-B: Remark on Algorithm 778: L-BFGS-B,\n      FORTRAN routines for large scale bound constrained optimization (2011),\n      ACM Transactions on Mathematical Software, 38, 1.\n\n    "
    if approx_grad:
        fun = func
        jac = None
    elif (fprime is None):
        fun = MemoizeJac(func)
        jac = fun.derivative
    else:
        fun = func
        jac = fprime
    if (disp is None):
        disp = iprint
    opts = {
        'disp': disp,
        'iprint': iprint,
        'maxcor': m,
        'ftol': (factr * np.finfo(float).eps),
        'gtol': pgtol,
        'eps': epsilon,
        'maxfun': maxfun,
        'maxiter': maxiter,
        'callback': callback,
        'maxls': maxls,
    }
    res = _minimize_lbfgsb(fun, x0, args=args, jac=jac, bounds=bounds, **opts)
    d = {
        'grad': res['jac'],
        'task': res['message'],
        'funcalls': res['nfev'],
        'nit': res['nit'],
        'warnflag': res['status'],
    }
    f = res['fun']
    x = res['x']
    return (x, f, d)