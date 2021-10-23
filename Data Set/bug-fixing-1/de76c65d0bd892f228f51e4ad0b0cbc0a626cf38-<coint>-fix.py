

def coint(y1, y2, regression='c'):
    '\n    This is a simple cointegration test. Uses unit-root test on residuals to\n    test for cointegrated relationship\n\n    See Hamilton (1994) 19.2\n\n    Parameters\n    ----------\n    y1 : array_like, 1d\n        first element in cointegrating vector\n    y2 : array_like\n        remaining elements in cointegrating vector\n    c : str {\'c\'}\n        Included in regression\n        * \'c\' : Constant\n\n    Returns\n    -------\n    coint_t : float\n        t-statistic of unit-root test on residuals\n    pvalue : float\n        MacKinnon\'s approximate p-value based on MacKinnon (1994)\n    crit_value : dict\n        Critical values for the test statistic at the 1 %, 5 %, and 10 %\n        levels.\n\n    Notes\n    -----\n    The Null hypothesis is that there is no cointegration, the alternative\n    hypothesis is that there is cointegrating relationship. If the pvalue is\n    small, below a critical size, then we can reject the hypothesis that there\n    is no cointegrating relationship.\n\n    P-values are obtained through regression surface approximation from\n    MacKinnon 1994.\n\n    References\n    ----------\n    MacKinnon, J.G. 1994.  "Approximate asymptotic distribution functions for\n        unit-root and cointegration tests.  `Journal of Business and Economic\n        Statistics` 12, 167-76.\n\n    '
    regression = regression.lower()
    if (regression not in ['c', 'nc', 'ct', 'ctt']):
        raise ValueError(('regression option %s not understood' % regression))
    y1 = np.asarray(y1)
    y2 = np.asarray(y2)
    if (regression == 'c'):
        y2 = add_constant(y2, prepend=False)
    st1_resid = OLS(y1, y2).fit().resid
    lgresid_cons = add_constant(st1_resid[0:(- 1)], prepend=False)
    uroot_reg = OLS(st1_resid[1:], lgresid_cons).fit()
    coint_t = ((uroot_reg.params[0] - 1) / uroot_reg.bse[0])
    pvalue = mackinnonp(coint_t, regression='c', N=2, lags=None)
    crit_value = mackinnoncrit(N=1, regression='c', nobs=len(y1))
    return (coint_t, pvalue, crit_value)
