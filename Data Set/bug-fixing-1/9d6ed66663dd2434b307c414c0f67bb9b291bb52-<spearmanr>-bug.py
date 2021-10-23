

def spearmanr(x, y, use_ties=True):
    '\n    Calculates a Spearman rank-order correlation coefficient and the p-value\n    to test for non-correlation.\n\n    The Spearman correlation is a nonparametric measure of the linear\n    relationship between two datasets. Unlike the Pearson correlation, the\n    Spearman correlation does not assume that both datasets are normally\n    distributed. Like other correlation coefficients, this one varies\n    between -1 and +1 with 0 implying no correlation. Correlations of -1 or\n    +1 imply an exact linear relationship. Positive correlations imply that\n    as `x` increases, so does `y`. Negative correlations imply that as `x`\n    increases, `y` decreases.\n\n    Missing values are discarded pair-wise: if a value is missing in `x`, the\n    corresponding value in `y` is masked.\n\n    The p-value roughly indicates the probability of an uncorrelated system\n    producing datasets that have a Spearman correlation at least as extreme\n    as the one computed from these datasets. The p-values are not entirely\n    reliable but are probably reasonable for datasets larger than 500 or so.\n\n    Parameters\n    ----------\n    x : array_like\n        The length of `x` must be > 2.\n    y : array_like\n        The length of `y` must be > 2.\n    use_ties : bool, optional\n        Whether the correction for ties should be computed.\n\n    Returns\n    -------\n    correlation : float\n        Spearman correlation coefficient\n    pvalue : float\n        2-tailed p-value.\n\n    References\n    ----------\n    [CRCProbStat2000] section 14.7\n\n    '
    (x, y, n) = _chk_size(x, y)
    (x, y) = (x.ravel(), y.ravel())
    m = ma.mask_or(ma.getmask(x), ma.getmask(y))
    n -= m.sum()
    if (m is not nomask):
        x = ma.array(x, mask=m, copy=True)
        y = ma.array(y, mask=m, copy=True)
    df = (n - 2)
    if (df < 0):
        raise ValueError('The input must have at least 3 entries!')
    rankx = rankdata(x)
    ranky = rankdata(y)
    dsq = np.add.reduce(((rankx - ranky) ** 2))
    if use_ties:
        xties = count_tied_groups(x)
        yties = count_tied_groups(y)
        corr_x = (np.sum((((v * k) * ((k ** 2) - 1)) for (k, v) in iteritems(xties))) / 12.0)
        corr_y = (np.sum((((v * k) * ((k ** 2) - 1)) for (k, v) in iteritems(yties))) / 12.0)
    else:
        corr_x = corr_y = 0
    denom = ((n * ((n ** 2) - 1)) / 6.0)
    if ((corr_x != 0) or (corr_y != 0)):
        rho = (((denom - dsq) - corr_x) - corr_y)
        rho /= ma.sqrt(((denom - (2 * corr_x)) * (denom - (2 * corr_y))))
    else:
        rho = (1.0 - (dsq / denom))
    t = (ma.sqrt(ma.divide(df, ((rho + 1.0) * (1.0 - rho)))) * rho)
    if (t is masked):
        prob = 0.0
    else:
        prob = _betai((0.5 * df), 0.5, (df / (df + (t * t))))
    return SpearmanrResult(rho, prob)
