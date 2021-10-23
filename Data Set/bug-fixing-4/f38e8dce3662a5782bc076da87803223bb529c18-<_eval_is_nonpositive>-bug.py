def _eval_is_nonpositive(self):
    from sympy.core.exprtools import _monotonic_sign
    if (not self.is_number):
        (c, a) = self.as_coeff_Add()
        if ((not c.is_zero) and a.is_nonpositive):
            v = _monotonic_sign(a)
            if (v is not None):
                s = (v + c)
                if s.is_nonpositive:
                    return True
                if (len(self.free_symbols) == 1):
                    v = _monotonic_sign(self)
                    if ((v is not None) and v.is_nonpositive):
                        return True