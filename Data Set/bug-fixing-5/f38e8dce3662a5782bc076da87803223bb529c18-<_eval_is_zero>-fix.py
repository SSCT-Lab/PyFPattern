def _eval_is_zero(self):
    if (self.is_commutative is False):
        return
    nz = []
    z = 0
    im_or_z = False
    im = False
    for a in self.args:
        if a.is_real:
            if a.is_zero:
                z += 1
            elif (a.is_zero is False):
                nz.append(a)
            else:
                return
        elif a.is_imaginary:
            im = True
        elif (S.ImaginaryUnit * a).is_real:
            im_or_z = True
        else:
            return
    if (z == len(self.args)):
        return True
    if (len(nz) == len(self.args)):
        return None
    b = self.func(*nz)
    if b.is_zero:
        if ((not im_or_z) and (not im)):
            return True
        if (im and (not im_or_z)):
            return False
    if (b.is_zero is False):
        return False