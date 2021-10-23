def _eval_is_positive(self):
    from sympy.core.exprtools import _monotonic_sign
    if self.is_number:
        return super(Add, self)._eval_is_positive()
    (c, a) = self.as_coeff_Add()
    if (not c.is_zero):
        v = _monotonic_sign(a)
        if (v is not None):
            s = (v + c)
            if ((s != self) and s.is_positive and a.is_nonnegative):
                return True
            if (len(self.free_symbols) == 1):
                v = _monotonic_sign(self)
                if ((v is not None) and (v != self) and v.is_positive):
                    return True
    pos = nonneg = nonpos = unknown_sign = False
    saw_INF = set()
    args = [a for a in self.args if (not a.is_zero)]
    if (not args):
        return False
    for a in args:
        ispos = a.is_positive
        infinite = a.is_infinite
        if infinite:
            saw_INF.add(fuzzy_or((ispos, a.is_nonnegative)))
            if ((True in saw_INF) and (False in saw_INF)):
                return
        if ispos:
            pos = True
            continue
        elif a.is_nonnegative:
            nonneg = True
            continue
        elif a.is_nonpositive:
            nonpos = True
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
    elif ((not nonpos) and (not nonneg) and pos):
        return True
    elif ((not nonpos) and pos):
        return True
    elif ((not pos) and (not nonneg)):
        return False