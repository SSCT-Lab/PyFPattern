def dblquad(func, a, b, gfun, hfun, args=(), epsabs=1.49e-08, epsrel=1.49e-08):
    '\n    Compute a double integral.\n\n    Return the double (definite) integral of ``func(y, x)`` from ``x = a..b``\n    and ``y = gfun(x)..hfun(x)``.\n\n    Parameters\n    ----------\n    func : callable\n        A Python function or method of at least two variables: y must be the\n        first argument and x the second argument.\n    a, b : float\n        The limits of integration in x: `a` < `b`\n    gfun : callable\n        The lower boundary curve in y which is a function taking a single\n        floating point argument (x) and returning a floating point result: a\n        lambda function can be useful here.\n    hfun : callable\n        The upper boundary curve in y (same requirements as `gfun`).\n    args : sequence, optional\n        Extra arguments to pass to `func`.\n    epsabs : float, optional\n        Absolute tolerance passed directly to the inner 1-D quadrature\n        integration. Default is 1.49e-8.\n    epsrel : float, optional\n        Relative tolerance of the inner 1-D integrals. Default is 1.49e-8.\n\n    Returns\n    -------\n    y : float\n        The resultant integral.\n    abserr : float\n        An estimate of the error.\n\n    See also\n    --------\n    quad : single integral\n    tplquad : triple integral\n    nquad : N-dimensional integrals\n    fixed_quad : fixed-order Gaussian quadrature\n    quadrature : adaptive Gaussian quadrature\n    odeint : ODE integrator\n    ode : ODE integrator\n    simps : integrator for sampled data\n    romb : integrator for sampled data\n    scipy.special : for coefficients and roots of orthogonal polynomials\n\n    '

    def temp_ranges(*args):
        return [gfun(args[0]), hfun(args[0])]
    return nquad(func, [temp_ranges, [a, b]], args=args)