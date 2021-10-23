def function_range(f, symbol, domain):
    "\n    Finds the range of a function in a given domain.\n    This method is limited by the ability to determine the singularities and\n    determine limits.\n\n    Examples\n    ========\n\n    >>> from sympy import Symbol, S, exp, log, pi, sqrt, sin, tan\n    >>> from sympy.sets import Interval\n    >>> from sympy.calculus.util import function_range\n    >>> x = Symbol('x')\n    >>> function_range(sin(x), x, Interval(0, 2*pi))\n    Interval(-1, 1)\n    >>> function_range(tan(x), x, Interval(-pi/2, pi/2))\n    Interval(-oo, oo)\n    >>> function_range(1/x, x, S.Reals)\n    Union(Interval.open(-oo, 0), Interval.open(0, oo))\n    >>> function_range(exp(x), x, S.Reals)\n    Interval.open(0, oo)\n    >>> function_range(log(x), x, S.Reals)\n    Interval(-oo, oo)\n    >>> function_range(sqrt(x), x , Interval(-5, 9))\n    Interval(0, 3)\n\n    "
    from sympy.solvers.solveset import solveset
    if isinstance(domain, EmptySet):
        return S.EmptySet
    period = periodicity(f, symbol)
    if (period is S.Zero):
        return FiniteSet(f.expand())
    if (period is not None):
        if isinstance(domain, Interval):
            if (domain.inf - domain.sup).is_infinite:
                domain = Interval(0, period)
        elif isinstance(domain, Union):
            for sub_dom in domain.args:
                if (isinstance(sub_dom, Interval) and (sub_dom.inf - sub_dom.sup).is_infinite):
                    domain = Interval(0, period)
    intervals = continuous_domain(f, symbol, domain)
    range_int = S.EmptySet
    if isinstance(intervals, (Interval, FiniteSet)):
        interval_iter = (intervals,)
    elif isinstance(intervals, Union):
        interval_iter = intervals.args
    else:
        raise NotImplementedError(filldedent('\n                Unable to find range for the given domain.\n                '))
    for interval in interval_iter:
        if isinstance(interval, FiniteSet):
            for singleton in interval:
                if (singleton in domain):
                    range_int += FiniteSet(f.subs(symbol, singleton))
        elif isinstance(interval, Interval):
            vals = S.EmptySet
            critical_points = S.EmptySet
            critical_values = S.EmptySet
            bounds = ((interval.left_open, interval.inf, '+'), (interval.right_open, interval.sup, '-'))
            for (is_open, limit_point, direction) in bounds:
                if is_open:
                    critical_values += FiniteSet(limit(f, symbol, limit_point, direction))
                    vals += critical_values
                else:
                    vals += FiniteSet(f.subs(symbol, limit_point))
            solution = solveset(f.diff(symbol), symbol, interval)
            if isinstance(solution, ConditionSet):
                raise NotImplementedError('Unable to find critical points for {}'.format(f))
            critical_points += solution
            for critical_point in critical_points:
                vals += FiniteSet(f.subs(symbol, critical_point))
            (left_open, right_open) = (False, False)
            if (critical_values is not S.EmptySet):
                if (critical_values.inf == vals.inf):
                    left_open = True
                if (critical_values.sup == vals.sup):
                    right_open = True
            range_int += Interval(vals.inf, vals.sup, left_open, right_open)
        else:
            raise NotImplementedError(filldedent('\n                Unable to find range for the given domain.\n                '))
    return range_int