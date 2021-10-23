def interpolating_spline(d, x, X, Y):
    'Return spline of degree ``d``, passing through the given ``X``\n    and ``Y`` values.\n\n    This function returns a piecewise function such that each part is\n    a polynomial of degree not greater than ``d``. The value of ``d``\n    must be 1 or greater and the values of ``X`` must be strictly\n    increasing.\n\n    Examples\n    ========\n\n    >>> from sympy import interpolating_spline\n    >>> from sympy.abc import x\n    >>> interpolating_spline(1, x, [1, 2, 4, 7], [3, 6, 5, 7])\n    Piecewise((3*x, (x >= 1) & (x <= 2)),\n            (7 - x/2, (x >= 2) & (x <= 4)),\n            (2*x/3 + 7/3, (x >= 4) & (x <= 7)))\n    >>> interpolating_spline(3, x, [-2, 0, 1, 3, 4], [4, 2, 1, 1, 3])\n    Piecewise((-x**3/36 - x**2/36 - 17*x/18 + 2, (x >= -2) & (x <= 1)),\n            (5*x**3/36 - 13*x**2/36 - 11*x/18 + 7/3, (x >= 1) & (x <= 4)))\n\n    See Also\n    ========\n\n    bsplines_basis_set, sympy.polys.specialpolys.interpolating_poly\n    '
    from sympy import symbols, Number, Dummy, Rational
    from sympy.solvers.solveset import linsolve
    from sympy.matrices.dense import Matrix
    d = sympify(d)
    if (not (d.is_Integer and d.is_positive)):
        raise ValueError(('Spline degree must be a positive integer, not %s.' % d))
    if (len(X) != len(Y)):
        raise ValueError('Number of X and Y coordinates must be the same.')
    if (len(X) < (d + 1)):
        raise ValueError('Degree must be less than the number of control points.')
    if (not all(((a < b) for (a, b) in zip(X, X[1:])))):
        raise ValueError('The x-coordinates must be strictly increasing.')
    if d.is_odd:
        j = ((d + 1) // 2)
        interior_knots = X[j:(- j)]
    else:
        j = (d // 2)
        interior_knots = [Rational((a + b), 2) for (a, b) in zip(X[j:((- j) - 1)], X[(j + 1):(- j)])]
    knots = ((([X[0]] * (d + 1)) + list(interior_knots)) + ([X[(- 1)]] * (d + 1)))
    basis = bspline_basis_set(d, knots, x)
    A = [[b.subs(x, v) for b in basis] for v in X]
    coeff = linsolve((Matrix(A), Matrix(Y)), symbols('c0:{}'.format(len(X)), cls=Dummy))
    coeff = list(coeff)[0]
    intervals = set([c for b in basis for (e, c) in b.args if (c != True)])
    ival = [e.atoms(Number) for e in intervals]
    ival = [list(sorted(e))[0] for e in ival]
    com = zip(ival, intervals)
    com = sorted(com, key=(lambda x: x[0]))
    intervals = [y for (x, y) in com]
    basis_dicts = [dict(((c, e) for (e, c) in b.args)) for b in basis]
    spline = []
    for i in intervals:
        piece = sum([(c * d.get(i, S.Zero)) for (c, d) in zip(coeff, basis_dicts)], S.Zero)
        spline.append((piece, i))
    return Piecewise(*spline)