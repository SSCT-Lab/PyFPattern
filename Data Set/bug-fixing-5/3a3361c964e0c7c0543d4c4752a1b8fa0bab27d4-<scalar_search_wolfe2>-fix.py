def scalar_search_wolfe2(phi, derphi, phi0=None, old_phi0=None, derphi0=None, c1=0.0001, c2=0.9, amax=None, extra_condition=None, maxiter=10):
    "Find alpha that satisfies strong Wolfe conditions.\n\n    alpha > 0 is assumed to be a descent direction.\n\n    Parameters\n    ----------\n    phi : callable phi(alpha)\n        Objective scalar function.\n    derphi : callable phi'(alpha)\n        Objective function derivative. Returns a scalar.\n    phi0 : float, optional\n        Value of phi at 0\n    old_phi0 : float, optional\n        Value of phi at previous point\n    derphi0 : float, optional\n        Value of derphi at 0\n    c1 : float, optional\n        Parameter for Armijo condition rule.\n    c2 : float, optional\n        Parameter for curvature condition rule.\n    amax : float, optional\n        Maximum step size\n    extra_condition : callable, optional\n        A callable of the form ``extra_condition(alpha, phi_value)``\n        returning a boolean. The line search accepts the value\n        of ``alpha`` only if this callable returns ``True``.\n        If the callable returns ``False`` for the step length,\n        the algorithm will continue with new iterates.\n        The callable is only called for iterates satisfying\n        the strong Wolfe conditions.\n    maxiter : int, optional\n        Maximum number of iterations to perform\n\n    Returns\n    -------\n    alpha_star : float or None\n        Best alpha, or None if the line search algorithm did not converge.\n    phi_star : float\n        phi at alpha_star\n    phi0 : float\n        phi at 0\n    derphi_star : float or None\n        derphi at alpha_star, or None if the line search algorithm\n        did not converge.\n\n    Notes\n    -----\n    Uses the line search algorithm to enforce strong Wolfe\n    conditions.  See Wright and Nocedal, 'Numerical Optimization',\n    1999, pg. 59-60.\n\n    For the zoom phase it uses an algorithm by [...].\n\n    "
    if (phi0 is None):
        phi0 = phi(0.0)
    if (derphi0 is None):
        derphi0 = derphi(0.0)
    alpha0 = 0
    if ((old_phi0 is not None) and (derphi0 != 0)):
        alpha1 = min(1.0, (((1.01 * 2) * (phi0 - old_phi0)) / derphi0))
    else:
        alpha1 = 1.0
    if (alpha1 < 0):
        alpha1 = 1.0
    phi_a1 = phi(alpha1)
    phi_a0 = phi0
    derphi_a0 = derphi0
    if (extra_condition is None):
        extra_condition = (lambda alpha, phi: True)
    for i in xrange(maxiter):
        if ((alpha1 == 0) or ((amax is not None) and (alpha0 == amax))):
            alpha_star = None
            phi_star = phi0
            phi0 = old_phi0
            derphi_star = None
            if (alpha1 == 0):
                msg = 'Rounding errors prevent the line search from converging'
            else:
                msg = ('The line search algorithm could not find a solution ' + ('less than or equal to amax: %s' % amax))
            warn(msg, LineSearchWarning)
            break
        if ((phi_a1 > (phi0 + ((c1 * alpha1) * derphi0))) or ((phi_a1 >= phi_a0) and (i > 1))):
            (alpha_star, phi_star, derphi_star) = _zoom(alpha0, alpha1, phi_a0, phi_a1, derphi_a0, phi, derphi, phi0, derphi0, c1, c2, extra_condition)
            break
        derphi_a1 = derphi(alpha1)
        if (abs(derphi_a1) <= ((- c2) * derphi0)):
            if extra_condition(alpha1, phi_a1):
                alpha_star = alpha1
                phi_star = phi_a1
                derphi_star = derphi_a1
                break
        if (derphi_a1 >= 0):
            (alpha_star, phi_star, derphi_star) = _zoom(alpha1, alpha0, phi_a1, phi_a0, derphi_a1, phi, derphi, phi0, derphi0, c1, c2, extra_condition)
            break
        alpha2 = (2 * alpha1)
        if (amax is not None):
            alpha2 = min(alpha2, amax)
        alpha0 = alpha1
        alpha1 = alpha2
        phi_a0 = phi_a1
        phi_a1 = phi(alpha1)
        derphi_a0 = derphi_a1
    else:
        alpha_star = alpha1
        phi_star = phi_a1
        derphi_star = None
        warn('The line search algorithm did not converge', LineSearchWarning)
    return (alpha_star, phi_star, phi0, derphi_star)