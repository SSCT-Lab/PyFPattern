

def _check_antecedents_inversion(g, x):
    ' Check antecedents for the laplace inversion integral. '
    from sympy import re, im, Or, And, Eq, exp, I, Add, nan, Ne
    _debug('Checking antecedents for inversion:')
    z = g.argument
    (_, e) = _get_coeff_exp(z, x)
    if (e < 0):
        _debug('  Flipping G.')
        return _check_antecedents_inversion(_flip_g(g), x)

    def statement_half(a, b, c, z, plus):
        (coeff, exponent) = _get_coeff_exp(z, x)
        a *= exponent
        b *= (coeff ** c)
        c *= exponent
        conds = []
        wp = (b * exp((((I * re(c)) * pi) / 2)))
        wm = (b * exp(((((- I) * re(c)) * pi) / 2)))
        if plus:
            w = wp
        else:
            w = wm
        conds += [And(Or(Eq(b, 0), (re(c) <= 0)), (re(a) <= (- 1)))]
        conds += [And(Ne(b, 0), Eq(im(c), 0), (re(c) > 0), (re(w) < 0))]
        conds += [And(Ne(b, 0), Eq(im(c), 0), (re(c) > 0), (re(w) <= 0), (re(a) <= (- 1)))]
        return Or(*conds)

    def statement(a, b, c, z):
        ' Provide a convergence statement for z**a * exp(b*z**c),\n             c/f sphinx docs. '
        return And(statement_half(a, b, c, z, True), statement_half(a, b, c, z, False))
    (m, n, p, q) = S([len(g.bm), len(g.an), len(g.ap), len(g.bq)])
    tau = ((m + n) - p)
    nu = ((q - m) - n)
    rho = ((tau - nu) / 2)
    sigma = (q - p)
    if (sigma == 1):
        epsilon = (S(1) / 2)
    elif (sigma > 1):
        epsilon = 1
    else:
        epsilon = nan
    theta = (((((1 - sigma) / 2) + Add(*g.bq)) - Add(*g.ap)) / sigma)
    delta = g.delta
    _debug(('  m=%s, n=%s, p=%s, q=%s, tau=%s, nu=%s, rho=%s, sigma=%s' % (m, n, p, q, tau, nu, rho, sigma)))
    _debug(('  epsilon=%s, theta=%s, delta=%s' % (epsilon, theta, delta)))
    if (not ((g.delta >= (e / 2)) or ((p >= 1) and (p >= q)))):
        _debug('  Computation not valid for these parameters.')
        return False
    for a in g.an:
        for b in g.bm:
            if ((a - b).is_integer and (a > b)):
                _debug('  Not a valid G function.')
                return False
    if (p >= q):
        _debug('  Using asymptotic Slater expansion.')
        return And(*[statement((a - 1), 0, 0, z) for a in g.an])

    def E(z):
        return And(*[statement((a - 1), 0, 0, z) for a in g.an])

    def H(z):
        return statement(theta, (- sigma), (1 / sigma), z)

    def Hp(z):
        return statement_half(theta, (- sigma), (1 / sigma), z, True)

    def Hm(z):
        return statement_half(theta, (- sigma), (1 / sigma), z, False)
    conds = []
    conds += [And((1 <= n), (p < q), (1 <= m), (((rho * pi) - delta) >= (pi / 2)), (delta > 0), E((z * exp(((I * pi) * (nu + 1))))))]
    conds += [And(((p + 1) <= m), ((m + 1) <= q), (delta > 0), (delta < (pi / 2)), (n == 0), (((((m - p) + 1) * pi) - delta) >= (pi / 2)), Hp((z * exp(((I * pi) * (q - m))))), Hm((z * exp((((- I) * pi) * (q - m))))))]
    conds += [And((p < q), (m == q), (n == 0), (delta > 0), ((((sigma + epsilon) * pi) - delta) >= (pi / 2)), H(z))]
    conds += [And(Or(And((p <= (q - 2)), (1 <= tau), (tau <= (sigma / 2))), And(((p + 1) <= (m + n)), ((m + n) <= ((p + q) / 2)))), (delta > 0), (delta < (pi / 2)), ((((tau + 1) * pi) - delta) >= (pi / 2)), Hp((z * exp(((I * pi) * nu)))), Hm((z * exp((((- I) * pi) * nu)))))]
    conds += [And((p < q), (1 <= m), (rho > 0), (delta > 0), ((delta + (rho * pi)) < (pi / 2)), ((((tau + epsilon) * pi) - delta) >= (pi / 2)), Hp((z * exp(((I * pi) * nu)))), Hm((z * exp((((- I) * pi) * nu)))))]
    conds += [(m == 0)]
    return Or(*conds)
