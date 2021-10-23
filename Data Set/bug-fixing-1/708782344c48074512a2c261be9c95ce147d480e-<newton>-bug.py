

def newton(func, x0, fprime=None, args=(), tol=1.48e-08, maxiter=50, fprime2=None):
    "\n    Find a zero using the Newton-Raphson or secant method.\n\n    Find a zero of the function `func` given a nearby starting point `x0`.\n    The Newton-Raphson method is used if the derivative `fprime` of `func`\n    is provided, otherwise the secant method is used.  If the second order\n    derivative `fprime2` of `func` is provided, then Halley's method is used.\n\n    Parameters\n    ----------\n    func : function\n        The function whose zero is wanted. It must be a function of a\n        single variable of the form f(x,a,b,c...), where a,b,c... are extra\n        arguments that can be passed in the `args` parameter.\n    x0 : float\n        An initial estimate of the zero that should be somewhere near the\n        actual zero.\n    fprime : function, optional\n        The derivative of the function when available and convenient. If it\n        is None (default), then the secant method is used.\n    args : tuple, optional\n        Extra arguments to be used in the function call.\n    tol : float, optional\n        The allowable error of the zero value.\n    maxiter : int, optional\n        Maximum number of iterations.\n    fprime2 : function, optional\n        The second order derivative of the function when available and\n        convenient. If it is None (default), then the normal Newton-Raphson\n        or the secant method is used. If it is not None, then Halley's method\n        is used.\n\n    Returns\n    -------\n    zero : float\n        Estimated location where function is zero.\n\n    See Also\n    --------\n    brentq, brenth, ridder, bisect\n    fsolve : find zeroes in n dimensions.\n\n    Notes\n    -----\n    The convergence rate of the Newton-Raphson method is quadratic,\n    the Halley method is cubic, and the secant method is\n    sub-quadratic.  This means that if the function is well behaved\n    the actual error in the estimated zero is approximately the square\n    (cube for Halley) of the requested tolerance up to roundoff\n    error. However, the stopping criterion used here is the step size\n    and there is no guarantee that a zero has been found. Consequently\n    the result should be verified. Safer algorithms are brentq,\n    brenth, ridder, and bisect, but they all require that the root\n    first be bracketed in an interval where the function changes\n    sign. The brentq algorithm is recommended for general use in one\n    dimensional problems when such an interval has been found.\n\n    Examples\n    --------\n\n    >>> def f(x):\n    ...     return (x**3 - 1)  # only one real root at x = 1\n    \n    >>> from scipy import optimize\n\n    ``fprime`` not provided, use secant method\n    \n    >>> root = optimize.newton(f, 1.5)\n    >>> root\n    1.0000000000000016\n    >>> root = optimize.newton(f, 1.5, fprime2=lambda x: 6 * x)\n    >>> root\n    1.0000000000000016\n\n    Only ``fprime`` provided, use Newton Raphson method\n    \n    >>> root = optimize.newton(f, 1.5, fprime=lambda x: 3 * x**2)\n    >>> root\n    1.0\n    \n    Both ``fprime2`` and ``fprime`` provided, use Halley's method\n\n    >>> root = optimize.newton(f, 1.5, fprime=lambda x: 3 * x**2,\n    ...                        fprime2=lambda x: 6 * x)\n    >>> root\n    1.0\n\n    "
    if (tol <= 0):
        raise ValueError(('tol too small (%g <= 0)' % tol))
    if (maxiter < 1):
        raise ValueError('maxiter must be greater than 0')
    if (fprime is not None):
        p0 = (1.0 * x0)
        fder2 = 0
        for iter in range(maxiter):
            myargs = ((p0,) + args)
            fder = fprime(*myargs)
            if (fder == 0):
                msg = 'derivative was zero.'
                warnings.warn(msg, RuntimeWarning)
                return p0
            fval = func(*myargs)
            newton_step = (fval / fder)
            if (fprime2 is None):
                p = (p0 - newton_step)
            else:
                fder2 = fprime2(*myargs)
                p = (p0 - (newton_step / (1.0 - (((0.5 * newton_step) * fder2) / fder))))
            if (abs((p - p0)) < tol):
                return p
            p0 = p
    else:
        p0 = x0
        if (x0 >= 0):
            p1 = ((x0 * (1 + 0.0001)) + 0.0001)
        else:
            p1 = ((x0 * (1 + 0.0001)) - 0.0001)
        q0 = func(*((p0,) + args))
        q1 = func(*((p1,) + args))
        for iter in range(maxiter):
            if (q1 == q0):
                if (p1 != p0):
                    msg = ('Tolerance of %s reached' % (p1 - p0))
                    warnings.warn(msg, RuntimeWarning)
                return ((p1 + p0) / 2.0)
            else:
                p = (p1 - ((q1 * (p1 - p0)) / (q1 - q0)))
            if (abs((p - p1)) < tol):
                return p
            p0 = p1
            q0 = q1
            p1 = p
            q1 = func(*((p1,) + args))
    msg = ('Failed to converge after %d iterations, value is %s' % (maxiter, p))
    raise RuntimeError(msg)
