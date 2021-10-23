@array_function_dispatch(_mirr_dispatcher)
def mirr(values, finance_rate, reinvest_rate):
    '\n    Modified internal rate of return.\n\n    .. deprecated:: 1.18\n\n       `mirr` is deprecated; for details, see NEP 32 [1]_.\n       Use the corresponding function in the numpy-financial library,\n       https://pypi.org/project/numpy-financial.\n\n    Parameters\n    ----------\n    values : array_like\n        Cash flows (must contain at least one positive and one negative\n        value) or nan is returned.  The first value is considered a sunk\n        cost at time zero.\n    finance_rate : scalar\n        Interest rate paid on the cash flows\n    reinvest_rate : scalar\n        Interest rate received on the cash flows upon reinvestment\n\n    Returns\n    -------\n    out : float\n        Modified internal rate of return\n\n    References\n    ----------\n    .. [1] NumPy Enhancement Proposal (NEP) 32,\n       https://numpy.org/neps/nep-0032-remove-financial-functions.html\n    '
    values = np.asarray(values)
    n = values.size
    if isinstance(finance_rate, Decimal):
        n = Decimal(n)
    pos = (values > 0)
    neg = (values < 0)
    if (not (pos.any() and neg.any())):
        return np.nan
    numer = np.abs(npv(reinvest_rate, (values * pos)))
    denom = np.abs(npv(finance_rate, (values * neg)))
    return ((((numer / denom) ** (1 / (n - 1))) * (1 + reinvest_rate)) - 1)