def fixed_quad(func, a, b, args=(), n=5):
    '\n    Compute a definite integral using fixed-order Gaussian quadrature.\n\n    Integrate `func` from `a` to `b` using Gaussian quadrature of\n    order `n`.\n\n    Parameters\n    ----------\n    func : callable\n        A Python function or method to integrate (must accept vector inputs).\n        If integrating a vector-valued function, the returned array must have\n        shape ``(..., len(x))``.\n    a : float\n        Lower limit of integration.\n    b : float\n        Upper limit of integration.\n    args : tuple, optional\n        Extra arguments to pass to function, if any.\n    n : int, optional\n        Order of quadrature integration. Default is 5.\n\n    Returns\n    -------\n    val : float\n        Gaussian quadrature approximation to the integral\n    none : None\n        Statically returned value of None\n\n\n    See Also\n    --------\n    quad : adaptive quadrature using QUADPACK\n    dblquad : double integrals\n    tplquad : triple integrals\n    romberg : adaptive Romberg quadrature\n    quadrature : adaptive Gaussian quadrature\n    romb : integrators for sampled data\n    simps : integrators for sampled data\n    cumtrapz : cumulative integration for sampled data\n    ode : ODE integrator\n    odeint : ODE integrator\n\n    Examples\n    --------\n    >>> from scipy import integrate\n    >>> f = lambda x: x**8\n    >>> integrate.fixed_quad(f, 0.0, 1.0, n=4)\n    (0.1110884353741496, None)\n    >>> integrate.fixed_quad(f, 0.0, 1.0, n=5)\n    (0.11111111111111102, None)\n    >>> print(1/9.0)  # analytical result\n    0.1111111111111111\n\n    >>> integrate.fixed_quad(np.cos, 0.0, np.pi/2, n=4)\n    (0.9999999771971152, None)\n    >>> integrate.fixed_quad(np.cos, 0.0, np.pi/2, n=5)\n    (1.000000000039565, None)\n    >>> np.sin(np.pi/2)-np.sin(0)  # analytical result\n    1.0\n\n    '
    (x, w) = _cached_roots_legendre(n)
    x = np.real(x)
    if (np.isinf(a) or np.isinf(b)):
        raise ValueError('Gaussian quadrature is only available for finite limits.')
    y = ((((b - a) * (x + 1)) / 2.0) + a)
    return ((((b - a) / 2.0) * np.sum((w * func(y, *args)), axis=(- 1))), None)