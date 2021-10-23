def simplify(self, x):
    'simplify(self, x)\n\n           Compute a simplified representation of the function using\n           property number 4.\n\n           x can be:\n\n           - a symbol\n\n           Examples\n           ========\n\n           >>> from sympy import DiracDelta\n           >>> from sympy.abc import x, y\n\n           >>> DiracDelta(x*y).simplify(x)\n           DiracDelta(x)/Abs(y)\n           >>> DiracDelta(x*y).simplify(y)\n           DiracDelta(y)/Abs(x)\n\n           >>> DiracDelta(x**2 + x - 2).simplify(x)\n           DiracDelta(x - 1)/3 + DiracDelta(x + 2)/3\n\n           See Also\n           ========\n\n           is_simple, Directdelta\n\n        '
    from sympy.polys.polyroots import roots
    if ((not self.args[0].has(x)) or ((len(self.args) > 1) and (self.args[1] != 0))):
        return self
    try:
        argroots = roots(self.args[0], x)
        result = 0
        valid = True
        darg = abs(diff(self.args[0], x))
        for (r, m) in argroots.items():
            if ((r.is_real is not False) and (m == 1)):
                result += (self.func((x - r)) / darg.subs(x, r))
            else:
                valid = False
                break
        if valid:
            return result
    except PolynomialError:
        pass
    return self