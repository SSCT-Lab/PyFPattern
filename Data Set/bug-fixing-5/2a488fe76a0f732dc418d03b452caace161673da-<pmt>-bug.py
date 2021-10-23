@array_function_dispatch(_pmt_dispatcher)
def pmt(rate, nper, pv, fv=0, when='end'):
    "\n    Compute the payment against loan principal plus interest.\n\n    .. deprecated:: 1.18\n\n       `pmt` is deprecated; see NEP 32::\n\n           https://numpy.org/neps/nep-0032-remove-financial-functions.html\n\n        Use the corresponding function in the numpy-financial library,\n        https://pypi.org/project/numpy-financial\n\n    Given:\n     * a present value, `pv` (e.g., an amount borrowed)\n     * a future value, `fv` (e.g., 0)\n     * an interest `rate` compounded once per period, of which\n       there are\n     * `nper` total\n     * and (optional) specification of whether payment is made\n       at the beginning (`when` = {'begin', 1}) or the end\n       (`when` = {'end', 0}) of each period\n\n    Return:\n       the (fixed) periodic payment.\n\n    Parameters\n    ----------\n    rate : array_like\n        Rate of interest (per period)\n    nper : array_like\n        Number of compounding periods\n    pv : array_like\n        Present value\n    fv : array_like,  optional\n        Future value (default = 0)\n    when : {{'begin', 1}, {'end', 0}}, {string, int}\n        When payments are due ('begin' (1) or 'end' (0))\n\n    Returns\n    -------\n    out : ndarray\n        Payment against loan plus interest.  If all input is scalar, returns a\n        scalar float.  If any input is array_like, returns payment for each\n        input element. If multiple inputs are array_like, they all must have\n        the same shape.\n\n    Notes\n    -----\n    The payment is computed by solving the equation::\n\n     fv +\n     pv*(1 + rate)**nper +\n     pmt*(1 + rate*when)/rate*((1 + rate)**nper - 1) == 0\n\n    or, when ``rate == 0``::\n\n      fv + pv + pmt * nper == 0\n\n    for ``pmt``.\n\n    Note that computing a monthly mortgage payment is only\n    one use for this function.  For example, pmt returns the\n    periodic deposit one must make to achieve a specified\n    future balance given an initial deposit, a fixed,\n    periodically compounded interest rate, and the total\n    number of periods.\n\n    References\n    ----------\n    .. [WRW] Wheeler, D. A., E. Rathke, and R. Weir (Eds.) (2009, May).\n       Open Document Format for Office Applications (OpenDocument)v1.2,\n       Part 2: Recalculated Formula (OpenFormula) Format - Annotated Version,\n       Pre-Draft 12. Organization for the Advancement of Structured Information\n       Standards (OASIS). Billerica, MA, USA. [ODT Document].\n       Available:\n       http://www.oasis-open.org/committees/documents.php\n       ?wg_abbrev=office-formulaOpenDocument-formula-20090508.odt\n\n    Examples\n    --------\n    What is the monthly payment needed to pay off a $200,000 loan in 15\n    years at an annual interest rate of 7.5%?\n\n    >>> np.pmt(0.075/12, 12*15, 200000)\n    -1854.0247200054619\n\n    In order to pay-off (i.e., have a future-value of 0) the $200,000 obtained\n    today, a monthly payment of $1,854.02 would be required.  Note that this\n    example illustrates usage of `fv` having a default value of 0.\n\n    "
    when = _convert_when(when)
    (rate, nper, pv, fv, when) = map(np.array, [rate, nper, pv, fv, when])
    temp = ((1 + rate) ** nper)
    mask = (rate == 0)
    masked_rate = np.where(mask, 1, rate)
    fact = np.where((mask != 0), nper, (((1 + (masked_rate * when)) * (temp - 1)) / masked_rate))
    return ((- (fv + (pv * temp))) / fact)