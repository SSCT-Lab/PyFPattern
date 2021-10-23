def bspline_basis(d, knots, n, x):
    'The `n`-th B-spline at `x` of degree `d` with knots.\n\n    B-Splines are piecewise polynomials of degree `d` [1]_.  They are\n    defined on a set of knots, which is a sequence of integers or\n    floats.\n\n    The 0th degree splines have a value of one on a single interval:\n\n        >>> from sympy import bspline_basis\n        >>> from sympy.abc import x\n        >>> d = 0\n        >>> knots = range(5)\n        >>> bspline_basis(d, knots, 0, x)\n        Piecewise((1, (x >= 0) & (x <= 1)), (0, True))\n\n    For a given ``(d, knots)`` there are ``len(knots)-d-1`` B-splines\n    defined, that are indexed by ``n`` (starting at 0).\n\n    Here is an example of a cubic B-spline:\n\n        >>> bspline_basis(3, range(5), 0, x)\n        Piecewise((x**3/6, (x >= 0) & (x <= 1)),\n                  (-x**3/2 + 2*x**2 - 2*x + 2/3,\n                  (x >= 1) & (x <= 2)),\n                  (x**3/2 - 4*x**2 + 10*x - 22/3,\n                  (x >= 2) & (x <= 3)),\n                  (-x**3/6 + 2*x**2 - 8*x + 32/3,\n                  (x >= 3) & (x <= 4)),\n                  (0, True))\n\n    By repeating knot points, you can introduce discontinuities in the\n    B-splines and their derivatives:\n\n        >>> d = 1\n        >>> knots = [0, 0, 2, 3, 4]\n        >>> bspline_basis(d, knots, 0, x)\n        Piecewise((1 - x/2, (x >= 0) & (x <= 2)), (0, True))\n\n    It is quite time consuming to construct and evaluate B-splines. If\n    you need to evaluate a B-splines many times, it is best to\n    lambdify them first:\n\n        >>> from sympy import lambdify\n        >>> d = 3\n        >>> knots = range(10)\n        >>> b0 = bspline_basis(d, knots, 0, x)\n        >>> f = lambdify(x, b0)\n        >>> y = f(0.5)\n\n    See Also\n    ========\n\n    bsplines_basis_set\n\n    References\n    ==========\n\n    .. [1] https://en.wikipedia.org/wiki/B-spline\n\n    '
    knots = [sympify(k) for k in knots]
    d = int(d)
    n = int(n)
    n_knots = len(knots)
    n_intervals = (n_knots - 1)
    if (((n + d) + 1) > n_intervals):
        raise ValueError('n + d + 1 must not exceed len(knots) - 1')
    if (d == 0):
        result = Piecewise((S.One, Interval(knots[n], knots[(n + 1)]).contains(x)), (0, True))
    elif (d > 0):
        denom = (knots[((n + d) + 1)] - knots[(n + 1)])
        if (denom != S.Zero):
            B = ((knots[((n + d) + 1)] - x) / denom)
            b2 = bspline_basis((d - 1), knots, (n + 1), x)
        else:
            b2 = B = S.Zero
        denom = (knots[(n + d)] - knots[n])
        if (denom != S.Zero):
            A = ((x - knots[n]) / denom)
            b1 = bspline_basis((d - 1), knots, n, x)
        else:
            b1 = A = S.Zero
        result = _add_splines(A, b1, B, b2)
    else:
        raise ValueError(('degree must be non-negative: %r' % n))
    return result