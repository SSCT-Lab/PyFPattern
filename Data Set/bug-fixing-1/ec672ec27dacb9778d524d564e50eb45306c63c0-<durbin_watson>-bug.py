

def durbin_watson(resids, axis=0):
    '\n    Calculates the Durbin-Watson statistic\n\n    Parameters\n    -----------\n    resids : array-like\n\n    Returns\n    --------\n    dw : float, array-like\n\n    The Durbin-Watson statistic.\n\n    Notes\n    -----\n    The null hypothesis of the test is that there is no serial correlation.\n    The Durbin-Watson test statistics is defined as:\n\n    .. math::\n\n       \\sum_{t=2}^T((e_t - e_{t-1})^2)/\\sum_{t=1}^Te_t^2\n\n    The test statistic is approximately equal to 2*(1-r) where ``r`` is the\n    sample autocorrelation of the residuals. Thus, for r == 0, indicating no\n    serial correlation, the test statistic equals 2. This statistic will\n    always be between 0 and 4. The closer to 0 the statistic, the more\n    evidence for positive serial correlation. The closer to 4, the more\n    evidence for negative serial correlation.\n    '
    resids = np.asarray(resids)
    diff_resids = np.diff(resids, 1, axis=axis)
    dw = (np.sum((diff_resids ** 2), axis=axis) / np.sum((resids ** 2), axis=axis))
    return dw
