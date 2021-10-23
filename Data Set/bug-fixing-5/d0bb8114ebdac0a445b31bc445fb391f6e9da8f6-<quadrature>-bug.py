def quadrature(func, a, b, args=(), tol=1.49e-08, rtol=1.49e-08, maxiter=50, vec_func=True, miniter=1):
    '\n    Compute a definite integral using fixed-tolerance Gaussian quadrature.\n\n    Integrate `func` from `a` to `b` using Gaussian quadrature\n    with absolute tolerance `tol`.\n\n    Parameters\n    ----------\n    func : function\n        A Python function or method to integrate.\n    a : float\n        Lower limit of integration.\n    b : float\n        Upper limit of integration.\n    args : tuple, optional\n        Extra arguments to pass to function.\n    tol, rtol : float, optional\n        Iteration stops when error between last two iterates is less than\n        `tol` OR the relative change is less than `rtol`.\n    maxiter : int, optional\n        Maximum order of Gaussian quadrature.\n    vec_func : bool, optional\n        True or False if func handles arrays as arguments (is\n        a "vector" function). Default is True.\n    miniter : int, optional\n        Minimum order of Gaussian quadrature.\n\n    Returns\n    -------\n    val : float\n        Gaussian quadrature approximation (within tolerance) to integral.\n    err : float\n        Difference between last two estimates of the integral.\n\n    See also\n    --------\n    romberg: adaptive Romberg quadrature\n    fixed_quad: fixed-order Gaussian quadrature\n    quad: adaptive quadrature using QUADPACK\n    dblquad: double integrals\n    tplquad: triple integrals\n    romb: integrator for sampled data\n    simps: integrator for sampled data\n    cumtrapz: cumulative integration for sampled data\n    ode: ODE integrator\n    odeint: ODE integrator\n\n    '
    if (not isinstance(args, tuple)):
        args = (args,)
    vfunc = vectorize1(func, args, vec_func=vec_func)
    val = np.inf
    err = np.inf
    maxiter = max((miniter + 1), maxiter)
    for n in xrange(miniter, (maxiter + 1)):
        newval = fixed_quad(vfunc, a, b, (), n)[0]
        err = abs((newval - val))
        val = newval
        if ((err < tol) or (err < (rtol * abs(val)))):
            break
    else:
        warnings.warn(('maxiter (%d) exceeded. Latest difference = %e' % (maxiter, err)), AccuracyWarning)
    return (val, err)