@array_function_dispatch(_nper_dispatcher)
def nper(rate, pmt, pv, fv=0, when='end'):
    "\n    Compute the number of periodic payments.\n\n    .. deprecated:: 1.18\n\n       `nper` is deprecated; for details, see NEP 32 [1]_.\n       Use the corresponding function in the numpy-financial library,\n       https://pypi.org/project/numpy-financial.\n\n    :class:`decimal.Decimal` type is not supported.\n\n    Parameters\n    ----------\n    rate : array_like\n        Rate of interest (per period)\n    pmt : array_like\n        Payment\n    pv : array_like\n        Present value\n    fv : array_like, optional\n        Future value\n    when : {{'begin', 1}, {'end', 0}}, {string, int}, optional\n        When payments are due ('begin' (1) or 'end' (0))\n\n    Notes\n    -----\n    The number of periods ``nper`` is computed by solving the equation::\n\n     fv + pv*(1+rate)**nper + pmt*(1+rate*when)/rate*((1+rate)**nper-1) = 0\n\n    but if ``rate = 0`` then::\n\n     fv + pv + pmt*nper = 0\n\n    References\n    ----------\n    .. [1] NumPy Enhancement Proposal (NEP) 32,\n       https://numpy.org/neps/nep-0032-remove-financial-functions.html\n\n    Examples\n    --------\n    If you only had $150/month to pay towards the loan, how long would it take\n    to pay-off a loan of $8,000 at 7% annual interest?\n\n    >>> print(np.round(np.nper(0.07/12, -150, 8000), 5))\n    64.07335\n\n    So, over 64 months would be required to pay off the loan.\n\n    The same analysis could be done with several different interest rates\n    and/or payments and/or total amounts to produce an entire table.\n\n    >>> np.nper(*(np.ogrid[0.07/12: 0.08/12: 0.01/12,\n    ...                    -150   : -99     : 50    ,\n    ...                    8000   : 9001    : 1000]))\n    array([[[ 64.07334877,  74.06368256],\n            [108.07548412, 127.99022654]],\n           [[ 66.12443902,  76.87897353],\n            [114.70165583, 137.90124779]]])\n\n    "
    when = _convert_when(when)
    (rate, pmt, pv, fv, when) = map(np.asarray, [rate, pmt, pv, fv, when])
    use_zero_rate = False
    with np.errstate(divide='raise'):
        try:
            z = ((pmt * (1 + (rate * when))) / rate)
        except FloatingPointError:
            use_zero_rate = True
    if use_zero_rate:
        return (((- fv) + pv) / pmt)
    else:
        A = ((- (fv + pv)) / (pmt + 0))
        B = (np.log((((- fv) + z) / (pv + z))) / np.log((1 + rate)))
        return np.where((rate == 0), A, B)