def is_simple(self, x):
    'is_simple(self, x)\n\n           Tells whether the argument(args[0]) of DiracDelta is a linear\n           expression in x.\n\n           x can be:\n\n           - a symbol\n\n           Examples\n           ========\n\n           >>> from sympy import DiracDelta, cos\n           >>> from sympy.abc import x, y\n\n           >>> DiracDelta(x*y).is_simple(x)\n           True\n           >>> DiracDelta(x*y).is_simple(y)\n           True\n\n           >>> DiracDelta(x**2+x-2).is_simple(x)\n           False\n\n           >>> DiracDelta(cos(x)).is_simple(x)\n           False\n\n           See Also\n           ========\n\n           simplify, Directdelta\n\n        '
    p = self.args[0].as_poly(x)
    if p:
        return (p.degree() == 1)
    return False