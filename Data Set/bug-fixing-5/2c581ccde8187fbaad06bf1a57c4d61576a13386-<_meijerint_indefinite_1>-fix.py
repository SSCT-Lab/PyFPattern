def _meijerint_indefinite_1(f, x):
    ' Helper that does not attempt any substitution. '
    from sympy import Integral, piecewise_fold, nan, zoo
    _debug('Trying to compute the indefinite integral of', f, 'wrt', x)
    gs = _rewrite1(f, x)
    if (gs is None):
        return None
    (fac, po, gl, cond) = gs
    _debug(' could rewrite:', gs)
    res = S(0)
    for (C, s, g) in gl:
        (a, b) = _get_coeff_exp(g.argument, x)
        (_, c) = _get_coeff_exp(po, x)
        c += s
        fac_ = ((fac * C) / (b * (a ** ((1 + c) / b))))
        rho = (((c + 1) / b) - 1)
        t = _dummy('t', 'meijerint-indefinite', S(1))

        def tr(p):
            return [((a + rho) + 1) for a in p]
        if any(((b.is_integer and ((b <= 0) == True)) for b in tr(g.bm))):
            r = (- meijerg(tr(g.an), (tr(g.aother) + [1]), (tr(g.bm) + [0]), tr(g.bother), t))
        else:
            r = meijerg((tr(g.an) + [1]), tr(g.aother), tr(g.bm), (tr(g.bother) + [0]), t)
        place = 0
        if (((b < 0) == True) or f.subs(x, 0).has(nan, zoo)):
            place = None
        r = hyperexpand(r.subs(t, (a * (x ** b))), place=place)
        res += powdenest((fac_ * r), polar=True)

    def _clean(res):
        "This multiplies out superfluous powers of x we created, and chops off\n        constants:\n\n            >> _clean(x*(exp(x)/x - 1/x) + 3)\n            exp(x)\n\n        cancel is used before mul_expand since it is possible for an\n        expression to have an additive constant that doesn't become isolated\n        with simple expansion. Such a situation was identified in issue 6369:\n\n\n        >>> from sympy import sqrt, cancel\n        >>> from sympy.abc import x\n        >>> a = sqrt(2*x + 1)\n        >>> bad = (3*x*a**5 + 2*x - a**5 + 1)/a**2\n        >>> bad.expand().as_independent(x)[0]\n        0\n        >>> cancel(bad).expand().as_independent(x)[0]\n        1\n        "
        from sympy import cancel
        res = expand_mul(cancel(res), deep=False)
        return Add._from_args(res.as_coeff_add(x)[1])
    res = piecewise_fold(res)
    if res.is_Piecewise:
        newargs = []
        for (expr, cond) in res.args:
            expr = _my_unpolarify(_clean(expr))
            newargs += [(expr, cond)]
        res = Piecewise(*newargs)
    else:
        res = _my_unpolarify(_clean(res))
    return Piecewise((res, _my_unpolarify(cond)), (Integral(f, x), True))