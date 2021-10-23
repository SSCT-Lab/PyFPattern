@array_function_dispatch(_polyint_dispatcher)
def polyint(p, m=1, k=None):
    '\n    Return an antiderivative (indefinite integral) of a polynomial.\n\n    The returned order `m` antiderivative `P` of polynomial `p` satisfies\n    :math:`\\frac{d^m}{dx^m}P(x) = p(x)` and is defined up to `m - 1`\n    integration constants `k`. The constants determine the low-order\n    polynomial part\n\n    .. math:: \\frac{k_{m-1}}{0!} x^0 + \\ldots + \\frac{k_0}{(m-1)!}x^{m-1}\n\n    of `P` so that :math:`P^{(j)}(0) = k_{m-j-1}`.\n\n    Parameters\n    ----------\n    p : array_like or poly1d\n        Polynomial to integrate.\n        A sequence is interpreted as polynomial coefficients, see `poly1d`.\n    m : int, optional\n        Order of the antiderivative. (Default: 1)\n    k : list of `m` scalars or scalar, optional\n        Integration constants. They are given in the order of integration:\n        those corresponding to highest-order terms come first.\n\n        If ``None`` (default), all constants are assumed to be zero.\n        If `m = 1`, a single scalar can be given instead of a list.\n\n    See Also\n    --------\n    polyder : derivative of a polynomial\n    poly1d.integ : equivalent method\n\n    Examples\n    --------\n    The defining property of the antiderivative:\n\n    >>> p = np.poly1d([1,1,1])\n    >>> P = np.polyint(p)\n    >>> P\n    poly1d([ 0.33333333,  0.5       ,  1.        ,  0.        ])\n    >>> np.polyder(P) == p\n    True\n\n    The integration constants default to zero, but can be specified:\n\n    >>> P = np.polyint(p, 3)\n    >>> P(0)\n    0.0\n    >>> np.polyder(P)(0)\n    0.0\n    >>> np.polyder(P, 2)(0)\n    0.0\n    >>> P = np.polyint(p, 3, k=[6,5,3])\n    >>> P\n    poly1d([ 0.01666667,  0.04166667,  0.16666667,  3. ,  5. ,  3. ])\n\n    Note that 3 = 6 / 2!, and that the constants are given in the order of\n    integrations. Constant of the highest-order polynomial term comes first:\n\n    >>> np.polyder(P, 2)(0)\n    6.0\n    >>> np.polyder(P, 1)(0)\n    5.0\n    >>> P(0)\n    3.0\n\n    '
    m = int(m)
    if (m < 0):
        raise ValueError('Order of integral must be positive (see polyder)')
    if (k is None):
        k = NX.zeros(m, float)
    k = atleast_1d(k)
    if ((len(k) == 1) and (m > 1)):
        k = (k[0] * NX.ones(m, float))
    if (len(k) < m):
        raise ValueError('k must be a scalar or a rank-1 array of length 1 or >m.')
    truepoly = isinstance(p, poly1d)
    p = NX.asarray(p)
    if (m == 0):
        if truepoly:
            return poly1d(p)
        return p
    else:
        y = NX.concatenate((p.__truediv__(NX.arange(len(p), 0, (- 1))), [k[0]]))
        val = polyint(y, (m - 1), k=k[1:])
        if truepoly:
            return poly1d(val)
        return val