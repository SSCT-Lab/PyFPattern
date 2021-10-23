

def optimize(self):
    func = self.func
    (xa, xb, xc, fa, fb, fc, funcalls) = self.get_bracket_info()
    _mintol = self._mintol
    _cg = self._cg
    x = w = v = xb
    fw = fv = fx = func(*((x,) + self.args))
    if (xa < xc):
        a = xa
        b = xc
    else:
        a = xc
        b = xa
    deltax = 0.0
    funcalls = 1
    iter = 0
    while (iter < self.maxiter):
        tol1 = ((self.tol * numpy.abs(x)) + _mintol)
        tol2 = (2.0 * tol1)
        xmid = (0.5 * (a + b))
        if (numpy.abs((x - xmid)) < (tol2 - (0.5 * (b - a)))):
            break
        if (numpy.abs(deltax) <= tol1):
            if (x >= xmid):
                deltax = (a - x)
            else:
                deltax = (b - x)
            rat = (_cg * deltax)
        else:
            tmp1 = ((x - w) * (fx - fv))
            tmp2 = ((x - v) * (fx - fw))
            p = (((x - v) * tmp2) - ((x - w) * tmp1))
            tmp2 = (2.0 * (tmp2 - tmp1))
            if (tmp2 > 0.0):
                p = (- p)
            tmp2 = numpy.abs(tmp2)
            dx_temp = deltax
            deltax = rat
            if ((p > (tmp2 * (a - x))) and (p < (tmp2 * (b - x))) and (numpy.abs(p) < numpy.abs(((0.5 * tmp2) * dx_temp)))):
                rat = ((p * 1.0) / tmp2)
                u = (x + rat)
                if (((u - a) < tol2) or ((b - u) < tol2)):
                    if ((xmid - x) >= 0):
                        rat = tol1
                    else:
                        rat = (- tol1)
            else:
                if (x >= xmid):
                    deltax = (a - x)
                else:
                    deltax = (b - x)
                rat = (_cg * deltax)
        if (numpy.abs(rat) < tol1):
            if (rat >= 0):
                u = (x + tol1)
            else:
                u = (x - tol1)
        else:
            u = (x + rat)
        fu = func(*((u,) + self.args))
        funcalls += 1
        if (fu > fx):
            if (u < x):
                a = u
            else:
                b = u
            if ((fu <= fw) or (w == x)):
                v = w
                w = u
                fv = fw
                fw = fu
            elif ((fu <= fv) or (v == x) or (v == w)):
                v = u
                fv = fu
        else:
            if (u >= x):
                a = x
            else:
                b = x
            v = w
            w = x
            x = u
            fv = fw
            fw = fx
            fx = fu
        iter += 1
    self.xmin = x
    self.fval = fx
    self.iter = iter
    self.funcalls = funcalls
