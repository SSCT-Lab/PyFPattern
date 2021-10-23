def fmin_bfgs(f, x0, fprime=None, args=(), gtol=1e-05, norm=Inf, epsilon=_epsilon, maxiter=None, full_output=0, disp=1, retall=0, callback=None):
    "\n    Minimize a function using the BFGS algorithm.\n\n    Parameters\n    ----------\n    f : callable f(x,*args)\n        Objective function to be minimized.\n    x0 : ndarray\n        Initial guess.\n    fprime : callable f'(x,*args), optional\n        Gradient of f.\n    args : tuple, optional\n        Extra arguments passed to f and fprime.\n    gtol : float, optional\n        Gradient norm must be less than gtol before successful termination.\n    norm : float, optional\n        Order of norm (Inf is max, -Inf is min)\n    epsilon : int or ndarray, optional\n        If fprime is approximated, use this value for the step size.\n    callback : callable, optional\n        An optional user-supplied function to call after each\n        iteration.  Called as callback(xk), where xk is the\n        current parameter vector.\n    maxiter : int, optional\n        Maximum number of iterations to perform.\n    full_output : bool, optional\n        If True,return fopt, func_calls, grad_calls, and warnflag\n        in addition to xopt.\n    disp : bool, optional\n        Print convergence message if True.\n    retall : bool, optional\n        Return a list of results at each iteration if True.\n\n    Returns\n    -------\n    xopt : ndarray\n        Parameters which minimize f, i.e. f(xopt) == fopt.\n    fopt : float\n        Minimum value.\n    gopt : ndarray\n        Value of gradient at minimum, f'(xopt), which should be near 0.\n    Bopt : ndarray\n        Value of 1/f''(xopt), i.e. the inverse hessian matrix.\n    func_calls : int\n        Number of function_calls made.\n    grad_calls : int\n        Number of gradient calls made.\n    warnflag : integer\n        1 : Maximum number of iterations exceeded.\n        2 : Gradient and/or function calls not changing.\n    allvecs  :  list\n        The value of xopt at each iteration.  Only returned if retall is True.\n\n    See also\n    --------\n    minimize: Interface to minimization algorithms for multivariate\n        functions. See the 'BFGS' `method` in particular.\n\n    Notes\n    -----\n    Optimize the function, f, whose gradient is given by fprime\n    using the quasi-Newton method of Broyden, Fletcher, Goldfarb,\n    and Shanno (BFGS)\n\n    References\n    ----------\n    Wright, and Nocedal 'Numerical Optimization', 1999, pg. 198.\n\n    "
    opts = {
        'gtol': gtol,
        'norm': norm,
        'eps': epsilon,
        'disp': disp,
        'maxiter': maxiter,
        'return_all': retall,
    }
    res = _minimize_bfgs(f, x0, args, fprime, callback=callback, **opts)
    if full_output:
        retlist = (res['x'], res['fun'], res['jac'], res['hess_inv'], res['nfev'], res['njev'], res['status'])
        if retall:
            retlist += (res['allvecs'],)
        return retlist
    elif retall:
        return (res['x'], res['allvecs'])
    else:
        return res['x']