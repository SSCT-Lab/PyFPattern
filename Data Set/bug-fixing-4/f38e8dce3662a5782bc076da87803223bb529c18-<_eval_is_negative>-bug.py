def _eval_is_negative(self):
    from sympy.core.exprtools import _monotonic_sign
    if self.is_number:
        return super(Add, self)._eval_is_negative()
    (c, a) = self.as_coeff_Add()
    if (not c.is_zero):
        v = _monotonic_sign(a)
        if (v is not None):
            s = (v + c)
            if (s.is_negative and a.is_nonpositive):
                return True
            if (len(self.free_symbols) == 1):
                v = _monotonic_sign(self)
                if ((v is not None) and v.is_negative):
                    return True
    neg = nonpos = nonneg = unknown_sign = False
    saw_INF = set()
    args = [a for a in self.args if (not a.is_zero)]
    if (not args):
        return False
    for a in args:
        isneg = a.is_negative
        infinite = a.is_infinite
        if infinite:
            saw_INF.add(fuzzy_or((isneg, a.is_nonpositive)))
            if ((True in saw_INF) and (False in saw_INF)):
                return
        if isneg:
            neg = True
            continue
        elif a.is_nonpositive:
            nonpos = True
            continue
        elif a.is_nonnegative:
            nonneg = True
            continue
        if (infinite is None):
            return
        unknown_sign = True
    if saw_INF:
        if (len(saw_INF) > 1):
            return
        return saw_INF.pop()
    elif unknown_sign:
        return
    elif ((not nonneg) and (not nonpos) and neg):
        return True
    elif ((not nonneg) and neg):
        return True
    elif ((not neg) and (not nonpos)):
        return False