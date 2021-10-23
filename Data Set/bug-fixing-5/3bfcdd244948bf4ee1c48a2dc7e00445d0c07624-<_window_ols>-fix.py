def _window_ols(y, x, window=None, window_type=None, min_periods=None):
    '\n    Minimal replacement for pandas ols that provides the required features\n\n    Parameters\n    ----------\n    y : pd.Series\n        Endogenous variable\n    x : pd.DataFrame\n        Exogenous variables, always adds a constant\n    window: {None, int}\n\n    window_type : {str, int}\n    min_periods : {None, int}\n\n    Returns\n    -------\n    results : Bunch\n        Bunch containing parameters (beta), R-squared (r2), nobs and\n        residuals (resid)\n    '
    if (window_type == FULL_SAMPLE):
        window_type = 'full_sample'
    elif (window_type == ROLLING):
        window_type = 'rolling'
    elif (window_type == EXPANDING):
        window_type = 'expanding'
    if ((window_type in ('rolling', 'expanding')) and (window is None)):
        window = y.shape[0]
    min_periods = (1 if (min_periods is None) else min_periods)
    window_type = ('full_sample' if (window is None) else window_type)
    window_type = ('rolling' if (window_type is None) else window_type)
    if (window_type == 'rolling'):
        min_periods = window
    if (window_type not in ('full_sample', 'rolling', 'expanding')):
        raise ValueError('Unknown window_type')
    x = x.copy()
    x['intercept'] = 1.0
    bunch = Bunch()
    if (window_type == 'full_sample'):
        missing = (y.isnull() | x.isnull().any(1))
        y = y.loc[(~ missing)]
        x = x.loc[(~ missing)]
        res = OLS(y, x).fit()
        bunch['beta'] = res.params
        bunch['r2'] = res.rsquared
        bunch['nobs'] = res.nobs
        bunch['resid'] = res.resid
        return bunch
    index = y.index
    columns = x.columns
    n = y.shape[0]
    k = x.shape[1]
    beta = pd.DataFrame(np.zeros((n, k)), columns=columns, index=index)
    r2 = pd.Series(np.zeros(n), index=index)
    nobs = r2.copy().astype(np.int)
    resid = r2.copy()
    valid = r2.copy().astype(np.bool)
    if (window_type == 'rolling'):
        start = window
    else:
        start = min_periods
    for i in range(start, (y.shape[0] + 1)):
        if (window_type == 'rolling'):
            left = max(0, (i - window))
            sel = slice(left, i)
        else:
            sel = slice(i)
        _y = y[sel]
        _x = x[sel]
        missing = (_y.isnull() | _x.isnull().any(1))
        if missing.any():
            if ((~ missing).sum() < min_periods):
                continue
            else:
                _y = _y.loc[(~ missing)]
                _x = _x.loc[(~ missing)]
        if (_y.shape[0] <= _x.shape[1]):
            continue
        if ((window_type == 'expanding') and missing.values[(- 1)]):
            continue
        res = OLS(_y, _x).fit()
        valid.iloc[(i - 1)] = True
        beta.iloc[(i - 1)] = res.params
        r2.iloc[(i - 1)] = res.rsquared
        nobs.iloc[(i - 1)] = int(res.nobs)
        resid.iloc[(i - 1)] = res.resid.iloc[(- 1)]
    bunch['beta'] = beta.loc[valid]
    bunch['r2'] = r2.loc[valid]
    bunch['nobs'] = nobs.loc[valid]
    bunch['resid'] = resid.loc[valid]
    return bunch