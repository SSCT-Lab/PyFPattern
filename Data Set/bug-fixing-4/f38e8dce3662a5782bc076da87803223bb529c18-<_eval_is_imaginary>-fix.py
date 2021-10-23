def _eval_is_imaginary(self):
    nz = []
    im_I = []
    for a in self.args:
        if a.is_real:
            if a.is_zero:
                pass
            elif (a.is_zero is False):
                nz.append(a)
            else:
                return
        elif a.is_imaginary:
            im_I.append((a * S.ImaginaryUnit))
        elif (S.ImaginaryUnit * a).is_real:
            im_I.append((a * S.ImaginaryUnit))
        else:
            return
    b = self.func(*nz)
    if b.is_zero:
        return fuzzy_not(self.func(*im_I).is_zero)
    elif (b.is_zero is False):
        return False