def scalar_search_wolfe1(phi, derphi, phi0=None, old_phi0=None, derphi0=None, c1=0.0001, c2=0.9, amax=50, amin=1e-08, xtol=1e-14):
    '\n    Scalar function search for alpha that satisfies strong Wolfe conditions\n\n    alpha > 0 is assumed to be a descent direction.\n\n    Parameters\n    ----------\n    phi : callable phi(alpha)\n        Function at point `alpha`\n    derphi : callable dphi(alpha)\n        Derivative `d phi(alpha)/ds`. Returns a scalar.\n\n    phi0 : float, optional\n        Value of `f` at 0\n    old_phi0 : float, optional\n        Value of `f` at the previous point\n    derphi0 : float, optional\n        Value `derphi` at 0\n    c1, c2 : float, optional\n        Wolfe parameters\n    amax, amin : float, optional\n        Maximum and minimum step size\n    xtol : float, optional\n        Relative tolerance for an acceptable step.\n\n    Returns\n    -------\n    alpha : float\n        Step size, or None if no suitable step was found\n    phi : float\n        Value of `phi` at the new point `alpha`\n    phi0 : float\n        Value of `phi` at `alpha=0`\n\n    Notes\n    -----\n    Uses routine DCSRCH from MINPACK.\n\n    '
    if (phi0 is None):
        phi0 = phi(0.0)
    if (derphi0 is None):
        derphi0 = derphi(0.0)
    if ((old_phi0 is not None) and (derphi0 != 0)):
        alpha1 = min(1.0, (((1.01 * 2) * (phi0 - old_phi0)) / derphi0))
        if (alpha1 < 0):
            alpha1 = 1.0
    else:
        alpha1 = 1.0
    phi1 = phi0
    derphi1 = derphi0
    isave = np.zeros((2,), np.intc)
    dsave = np.zeros((13,), float)
    task = b'START'
    maxiter = 100
    for i in xrange(maxiter):
        (stp, phi1, derphi1, task) = minpack2.dcsrch(alpha1, phi1, derphi1, c1, c2, xtol, task, amin, amax, isave, dsave)
        if (task[:2] == b'FG'):
            alpha1 = stp
            phi1 = phi(stp)
            derphi1 = derphi(stp)
        else:
            break
    else:
        stp = None
    if ((task[:5] == b'ERROR') or (task[:4] == b'WARN')):
        stp = None
    return (stp, phi1, phi0)