

def is_convergent(self):
    "Checks for the convergence of a Sum.\n\n        We divide the study of convergence of infinite sums and products in\n        two parts.\n\n        First Part:\n        One part is the question whether all the terms are well defined, i.e.,\n        they are finite in a sum and also non-zero in a product. Zero\n        is the analogy of (minus) infinity in products as :math:`e^{-\\infty} = 0`.\n\n        Second Part:\n        The second part is the question of convergence after infinities,\n        and zeros in products, have been omitted assuming that their number\n        is finite. This means that we only consider the tail of the sum or\n        product, starting from some point after which all terms are well\n        defined.\n\n        For example, in a sum of the form:\n\n        .. math::\n\n            \\sum_{1 \\leq i < \\infty} \\frac{1}{n^2 + an + b}\n\n        where a and b are numbers. The routine will return true, even if there\n        are infinities in the term sequence (at most two). An analogous\n        product would be:\n\n        .. math::\n\n            \\prod_{1 \\leq i < \\infty} e^{\\frac{1}{n^2 + an + b}}\n\n        This is how convergence is interpreted. It is concerned with what\n        happens at the limit. Finding the bad terms is another independent\n        matter.\n\n        Note: It is responsibility of user to see that the sum or product\n        is well defined.\n\n        There are various tests employed to check the convergence like\n        divergence test, root test, integral test, alternating series test,\n        comparison tests, Dirichlet tests. It returns true if Sum is convergent\n        and false if divergent and NotImplementedError if it can not be checked.\n\n        References\n        ==========\n\n        .. [1] https://en.wikipedia.org/wiki/Convergence_tests\n\n        Examples\n        ========\n\n        >>> from sympy import factorial, S, Sum, Symbol, oo\n        >>> n = Symbol('n', integer=True)\n        >>> Sum(n/(n - 1), (n, 4, 7)).is_convergent()\n        True\n        >>> Sum(n/(2*n + 1), (n, 1, oo)).is_convergent()\n        False\n        >>> Sum(factorial(n)/5**n, (n, 1, oo)).is_convergent()\n        False\n        >>> Sum(1/n**(S(6)/5), (n, 1, oo)).is_convergent()\n        True\n\n        See Also\n        ========\n\n        Sum.is_absolutely_convergent()\n\n        Product.is_convergent()\n        "
    from sympy import Interval, Integral, Limit, log, symbols, Ge, Gt, simplify
    (p, q) = symbols('p q', cls=Wild)
    sym = self.limits[0][0]
    lower_limit = self.limits[0][1]
    upper_limit = self.limits[0][2]
    sequence_term = self.function
    if (len(sequence_term.free_symbols) > 1):
        raise NotImplementedError('convergence checking for more than one symbol containing series is not handled')
    if (lower_limit.is_finite and upper_limit.is_finite):
        return S.true
    if (lower_limit is S.NegativeInfinity):
        if (upper_limit is S.Infinity):
            return (Sum(sequence_term, (sym, 0, S.Infinity)).is_convergent() and Sum(sequence_term, (sym, S.NegativeInfinity, 0)).is_convergent())
        sequence_term = simplify(sequence_term.xreplace({
            sym: (- sym),
        }))
        lower_limit = (- upper_limit)
        upper_limit = S.Infinity
    interval = Interval(lower_limit, upper_limit)
    if sequence_term.is_Piecewise:
        for func_cond in sequence_term.args:
            if ((func_cond[1].func is Ge) or (func_cond[1].func is Gt) or (func_cond[1] == True)):
                return Sum(func_cond[0], (sym, lower_limit, upper_limit)).is_convergent()
        return S.true
    try:
        lim_val = limit(sequence_term, sym, upper_limit)
        if (lim_val.is_number and (lim_val is not S.Zero)):
            return S.false
    except NotImplementedError:
        pass
    try:
        lim_val_abs = limit(abs(sequence_term), sym, upper_limit)
        if (lim_val_abs.is_number and (lim_val_abs is not S.Zero)):
            return S.false
    except NotImplementedError:
        pass
    order = O(sequence_term, (sym, S.Infinity))
    p1_series_test = order.expr.match((sym ** p))
    if (p1_series_test is not None):
        if (p1_series_test[p] < (- 1)):
            return S.true
        if (p1_series_test[p] > (- 1)):
            return S.false
    p2_series_test = order.expr.match(((1 / sym) ** p))
    if (p2_series_test is not None):
        if (p2_series_test[p] > 1):
            return S.true
        if (p2_series_test[p] < 1):
            return S.false
    lim = Limit((abs(sequence_term) ** (1 / sym)), sym, S.Infinity)
    lim_evaluated = lim.doit()
    if lim_evaluated.is_number:
        if (lim_evaluated < 1):
            return S.true
        if (lim_evaluated > 1):
            return S.false
    dict_val = sequence_term.match((((- 1) ** (sym + p)) * q))
    if ((not dict_val[p].has(sym)) and is_decreasing(dict_val[q], interval)):
        return S.true
    log_test = order.expr.match((1 / (log(sym) ** p)))
    if (log_test is not None):
        return S.false
    log_n_test = order.expr.match((1 / (sym * (log(sym) ** p))))
    if (log_n_test is not None):
        if (log_n_test[p] > 1):
            return S.true
        return S.false
    log_log_n_test = order.expr.match((1 / (sym * (log(sym) * (log(log(sym)) ** p)))))
    if (log_log_n_test is not None):
        if (log_log_n_test[p] > 1):
            return S.true
        return S.false
    n_log_test = order.expr.match((1 / ((sym ** p) * log(sym))))
    if (n_log_test is not None):
        if (n_log_test[p] > 1):
            return S.true
        return S.false
    if is_decreasing(sequence_term, interval):
        integral_val = Integral(sequence_term, (sym, lower_limit, upper_limit))
        try:
            integral_val_evaluated = integral_val.doit()
            if integral_val_evaluated.is_number:
                return S(integral_val_evaluated.is_finite)
        except NotImplementedError:
            pass
    if order.expr.is_Mul:
        (a_n, b_n) = (order.expr.args[0], order.expr.args[1])
        m = Dummy('m', integer=True)

        def _dirichlet_test(g_n):
            try:
                ing_val = limit(Sum(g_n, (sym, interval.inf, m)).doit(), m, S.Infinity)
                if ing_val.is_finite:
                    return S.true
            except NotImplementedError:
                pass
        if is_decreasing(a_n, interval):
            dirich1 = _dirichlet_test(b_n)
            if (dirich1 is not None):
                return dirich1
        if is_decreasing(b_n, interval):
            dirich2 = _dirichlet_test(a_n)
            if (dirich2 is not None):
                return dirich2
    raise NotImplementedError(('The algorithm to find the Sum convergence of %s is not yet implemented' % sequence_term))
