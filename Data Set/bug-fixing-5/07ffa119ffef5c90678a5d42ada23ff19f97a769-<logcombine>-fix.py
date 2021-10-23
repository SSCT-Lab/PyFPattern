def logcombine(expr, force=False):
    "\n    Takes logarithms and combines them using the following rules:\n\n    - log(x) + log(y) == log(x*y) if both are positive\n    - a*log(x) == log(x**a) if x is positive and a is real\n\n    If ``force`` is True then the assumptions above will be assumed to hold if\n    there is no assumption already in place on a quantity. For example, if\n    ``a`` is imaginary or the argument negative, force will not perform a\n    combination but if ``a`` is a symbol with no assumptions the change will\n    take place.\n\n    Examples\n    ========\n\n    >>> from sympy import Symbol, symbols, log, logcombine, I\n    >>> from sympy.abc import a, x, y, z\n    >>> logcombine(a*log(x) + log(y) - log(z))\n    a*log(x) + log(y) - log(z)\n    >>> logcombine(a*log(x) + log(y) - log(z), force=True)\n    log(x**a*y/z)\n    >>> x,y,z = symbols('x,y,z', positive=True)\n    >>> a = Symbol('a', real=True)\n    >>> logcombine(a*log(x) + log(y) - log(z))\n    log(x**a*y/z)\n\n    The transformation is limited to factors and/or terms that\n    contain logs, so the result depends on the initial state of\n    expansion:\n\n    >>> eq = (2 + 3*I)*log(x)\n    >>> logcombine(eq, force=True) == eq\n    True\n    >>> logcombine(eq.expand(), force=True)\n    log(x**2) + I*log(x**3)\n\n    See Also\n    ========\n\n    posify: replace all symbols with symbols having positive assumptions\n    sympy.core.function.expand_log: expand the logarithms of products\n        and powers; the opposite of logcombine\n\n    "

    def f(rv):
        if (not (rv.is_Add or rv.is_Mul)):
            return rv

        def gooda(a):
            return ((a is not S.NegativeOne) and (a.is_real or (force and (a.is_real is not False))))

        def goodlog(l):
            a = l.args[0]
            return (a.is_positive or (force and (a.is_nonpositive is not False)))
        other = []
        logs = []
        log1 = defaultdict(list)
        for a in Add.make_args(rv):
            if (isinstance(a, log) and goodlog(a)):
                log1[()].append(([], a))
            elif (not a.is_Mul):
                other.append(a)
            else:
                ot = []
                co = []
                lo = []
                for ai in a.args:
                    if (ai.is_Rational and (ai < 0)):
                        ot.append(S.NegativeOne)
                        co.append((- ai))
                    elif (isinstance(ai, log) and goodlog(ai)):
                        lo.append(ai)
                    elif gooda(ai):
                        co.append(ai)
                    else:
                        ot.append(ai)
                if (len(lo) > 1):
                    logs.append((ot, co, lo))
                elif lo:
                    log1[tuple(ot)].append((co, lo[0]))
                else:
                    other.append(a)
        if ((not logs) and all((((len(log1[k]) == 1) and (log1[k][0] == [])) for k in log1))):
            return rv
        for (o, e, l) in logs:
            l = list(ordered(l))
            e = log((l.pop(0).args[0] ** Mul(*e)))
            while l:
                li = l.pop(0)
                e = log((li.args[0] ** e))
            (c, l) = (Mul(*o), e)
            if isinstance(l, log):
                log1[(c,)].append(([], l))
            else:
                other.append((c * l))
        for k in list(log1.keys()):
            log1[Mul(*k)] = log(logcombine(Mul(*[(l.args[0] ** Mul(*c)) for (c, l) in log1.pop(k)]), force=force), evaluate=False)
        for k in ordered(list(log1.keys())):
            if (not (k in log1)):
                continue
            if ((- k) in log1):
                (num, den) = (k, (- k))
                if (num.count_ops() > den.count_ops()):
                    (num, den) = (den, num)
                other.append((num * log((log1.pop(num).args[0] / log1.pop(den).args[0]), evaluate=False)))
            else:
                other.append((k * log1.pop(k)))
        return Add(*other)
    return bottom_up(expr, f)