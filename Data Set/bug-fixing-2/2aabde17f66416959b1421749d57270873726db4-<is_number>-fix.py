

@property
def is_number(self):
    'Returns True if ``self`` has no free symbols.\n        It will be faster than ``if not self.free_symbols``, however, since\n        ``is_number`` will fail as soon as it hits a free symbol.\n\n        Examples\n        ========\n\n        >>> from sympy import log, Integral\n        >>> from sympy.abc import x\n\n        >>> x.is_number\n        False\n        >>> (2*x).is_number\n        False\n        >>> (2 + log(2)).is_number\n        True\n        >>> (2 + Integral(2, x)).is_number\n        False\n        >>> (2 + Integral(2, (x, 1, 2))).is_number\n        True\n\n        '
    return all((obj.is_number for obj in self.args))
