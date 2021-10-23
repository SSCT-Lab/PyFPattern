@array_function_dispatch(_rate_dispatcher)
def rate(nper, pmt, pv, fv, when='end', guess=None, tol=None, maxiter=100):
    "\n    Compute the rate of interest per period.\n\n    .. deprecated:: 1.18\n\n       `rate` is deprecated; for details, see NEP 32 [1]_.\n       Use the corresponding function in the numpy-financial library,\n       https://pypi.org/project/numpy-financial.\n\n    Parameters\n    ----------\n    nper : array_like\n        Number of compounding periods\n    pmt : array_like\n        Payment\n    pv : array_like\n        Present value\n    fv : array_like\n        Future value\n    when : {{'begin', 1}, {'end', 0}}, {string, int}, optional\n        When payments are due ('begin' (1) or 'end' (0))\n    guess : Number, optional\n        Starting guess for solving the rate of interest, default 0.1\n    tol : Number, optional\n        Required tolerance for the solution, default 1e-6\n    maxiter : int, optional\n        Maximum iterations in finding the solution\n\n    Notes\n    -----\n    The rate of interest is computed by iteratively solving the\n    (non-linear) equation::\n\n     fv + pv*(1+rate)**nper + pmt*(1+rate*when)/rate * ((1+rate)**nper - 1) = 0\n\n    for ``rate``.\n\n    References\n    ----------\n    .. [1] NumPy Enhancement Proposal (NEP) 32,\n       https://numpy.org/neps/nep-0032-remove-financial-functions.html\n    .. [2] Wheeler, D. A., E. Rathke, and R. Weir (Eds.) (2009, May).\n       Open Document Format for Office Applications (OpenDocument)v1.2,\n       Part 2: Recalculated Formula (OpenFormula) Format - Annotated Version,\n       Pre-Draft 12. Organization for the Advancement of Structured Information\n       Standards (OASIS). Billerica, MA, USA. [ODT Document].\n       Available:\n       http://www.oasis-open.org/committees/documents.php?wg_abbrev=office-formula\n       OpenDocument-formula-20090508.odt\n\n    "
    when = _convert_when(when)
    default_type = (Decimal if isinstance(pmt, Decimal) else float)
    if (guess is None):
        guess = default_type('0.1')
    if (tol is None):
        tol = default_type('1e-6')
    (nper, pmt, pv, fv, when) = map(np.asarray, [nper, pmt, pv, fv, when])
    rn = guess
    iterator = 0
    close = False
    while ((iterator < maxiter) and (not close)):
        rnp1 = (rn - _g_div_gp(rn, nper, pmt, pv, fv, when))
        diff = abs((rnp1 - rn))
        close = np.all((diff < tol))
        iterator += 1
        rn = rnp1
    if (not close):
        return (np.nan + rn)
    else:
        return rn