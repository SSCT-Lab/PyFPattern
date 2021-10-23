@array_function_dispatch(_irr_dispatcher)
def irr(values):
    '\n    Return the Internal Rate of Return (IRR).\n\n    .. deprecated:: 1.18\n\n       `irr` is deprecated; see NEP 32::\n\n           https://numpy.org/neps/nep-0032-remove-financial-functions.html\n\n        Use the corresponding function in the numpy-financial library,\n        https://pypi.org/project/numpy-financial\n\n    This is the "average" periodically compounded rate of return\n    that gives a net present value of 0.0; for a more complete explanation,\n    see Notes below.\n\n    :class:`decimal.Decimal` type is not supported.\n\n    Parameters\n    ----------\n    values : array_like, shape(N,)\n        Input cash flows per time period.  By convention, net "deposits"\n        are negative and net "withdrawals" are positive.  Thus, for\n        example, at least the first element of `values`, which represents\n        the initial investment, will typically be negative.\n\n    Returns\n    -------\n    out : float\n        Internal Rate of Return for periodic input values.\n\n    Notes\n    -----\n    The IRR is perhaps best understood through an example (illustrated\n    using np.irr in the Examples section below).  Suppose one invests 100\n    units and then makes the following withdrawals at regular (fixed)\n    intervals: 39, 59, 55, 20.  Assuming the ending value is 0, one\'s 100\n    unit investment yields 173 units; however, due to the combination of\n    compounding and the periodic withdrawals, the "average" rate of return\n    is neither simply 0.73/4 nor (1.73)^0.25-1.  Rather, it is the solution\n    (for :math:`r`) of the equation:\n\n    .. math:: -100 + \\frac{39}{1+r} + \\frac{59}{(1+r)^2}\n     + \\frac{55}{(1+r)^3} + \\frac{20}{(1+r)^4} = 0\n\n    In general, for `values` :math:`= [v_0, v_1, ... v_M]`,\n    irr is the solution of the equation: [G]_\n\n    .. math:: \\sum_{t=0}^M{\\frac{v_t}{(1+irr)^{t}}} = 0\n\n    References\n    ----------\n    .. [G] L. J. Gitman, "Principles of Managerial Finance, Brief," 3rd ed.,\n       Addison-Wesley, 2003, pg. 348.\n\n    Examples\n    --------\n    >>> round(np.irr([-100, 39, 59, 55, 20]), 5)\n    0.28095\n    >>> round(np.irr([-100, 0, 0, 74]), 5)\n    -0.0955\n    >>> round(np.irr([-100, 100, 0, -7]), 5)\n    -0.0833\n    >>> round(np.irr([-100, 100, 0, 7]), 5)\n    0.06206\n    >>> round(np.irr([-5, 10.5, 1, -8, 1]), 5)\n    0.0886\n\n    '
    res = np.roots(values[::(- 1)])
    mask = ((res.imag == 0) & (res.real > 0))
    if (not mask.any()):
        return np.nan
    res = res[mask].real
    rate = ((1 / res) - 1)
    rate = rate.item(np.argmin(np.abs(rate)))
    return rate