def cheb2poly(c):
    '\n    Convert a Chebyshev series to a polynomial.\n\n    Convert an array representing the coefficients of a Chebyshev series,\n    ordered from lowest degree to highest, to an array of the coefficients\n    of the equivalent polynomial (relative to the "standard" basis) ordered\n    from lowest to highest degree.\n\n    Parameters\n    ----------\n    c : array_like\n        1-D array containing the Chebyshev series coefficients, ordered\n        from lowest order term to highest.\n\n    Returns\n    -------\n    pol : ndarray\n        1-D array containing the coefficients of the equivalent polynomial\n        (relative to the "standard" basis) ordered from lowest order term\n        to highest.\n\n    See Also\n    --------\n    poly2cheb\n\n    Notes\n    -----\n    The easy way to do conversions between polynomial basis sets\n    is to use the convert method of a class instance.\n\n    Examples\n    --------\n    >>> from numpy import polynomial as P\n    >>> c = P.Chebyshev(range(4))\n    >>> c\n    Chebyshev([ 0.,  1.,  2.,  3.], [-1.,  1.])\n    >>> p = c.convert(kind=P.Polynomial)\n    >>> p\n    Polynomial([ -2.,  -8.,   4.,  12.], [-1.,  1.])\n    >>> P.cheb2poly(range(4))\n    array([ -2.,  -8.,   4.,  12.])\n\n    '
    from .polynomial import polyadd, polysub, polymulx
    [c] = pu.as_series([c])
    n = len(c)
    if (n < 3):
        return c
    else:
        c0 = c[(- 2)]
        c1 = c[(- 1)]
        for i in range((n - 1), 1, (- 1)):
            tmp = c0
            c0 = polysub(c[(i - 2)], c1)
            c1 = polyadd(tmp, (polymulx(c1) * 2))
        return polyadd(c0, polymulx(c1))