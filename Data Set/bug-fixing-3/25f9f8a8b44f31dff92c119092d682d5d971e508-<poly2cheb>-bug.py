def poly2cheb(pol):
    '\n    Convert a polynomial to a Chebyshev series.\n\n    Convert an array representing the coefficients of a polynomial (relative\n    to the "standard" basis) ordered from lowest degree to highest, to an\n    array of the coefficients of the equivalent Chebyshev series, ordered\n    from lowest to highest degree.\n\n    Parameters\n    ----------\n    pol : array_like\n        1-D array containing the polynomial coefficients\n\n    Returns\n    -------\n    c : ndarray\n        1-D array containing the coefficients of the equivalent Chebyshev\n        series.\n\n    See Also\n    --------\n    cheb2poly\n\n    Notes\n    -----\n    The easy way to do conversions between polynomial basis sets\n    is to use the convert method of a class instance.\n\n    Examples\n    --------\n    >>> from numpy import polynomial as P\n    >>> p = P.Polynomial(range(4))\n    >>> p\n    Polynomial([ 0.,  1.,  2.,  3.], domain=[-1,  1], window=[-1,  1])\n    >>> c = p.convert(kind=P.Chebyshev)\n    >>> c\n    Chebyshev([ 1.  ,  3.25,  1.  ,  0.75], domain=[-1,  1], window=[-1,  1])\n    >>> P.poly2cheb(range(4))\n    array([ 1.  ,  3.25,  1.  ,  0.75])\n\n    '
    [pol] = pu.as_series([pol])
    deg = (len(pol) - 1)
    res = 0
    for i in range(deg, (- 1), (- 1)):
        res = chebadd(chebmulx(res), pol[i])
    return res