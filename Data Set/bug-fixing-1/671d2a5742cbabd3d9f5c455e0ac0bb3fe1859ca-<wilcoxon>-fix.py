

def wilcoxon(x, y=None, zero_method='wilcox', correction=False, alternative='two-sided'):
    '\n    Calculate the Wilcoxon signed-rank test.\n\n    The Wilcoxon signed-rank test tests the null hypothesis that two\n    related paired samples come from the same distribution. In particular,\n    it tests whether the distribution of the differences x - y is symmetric\n    about zero. It is a non-parametric version of the paired T-test.\n\n    Parameters\n    ----------\n    x : array_like\n        Either the first set of measurements (in which case `y` is the second\n        set of measurements), or the differences between two sets of\n        measurements (in which case `y` is not to be specified.)  Must be\n        one-dimensional.\n    y : array_like, optional\n        Either the second set of measurements (if `x` is the first set of\n        measurements), or not specified (if `x` is the differences between\n        two sets of measurements.)  Must be one-dimensional.\n    zero_method : {"pratt", "wilcox", "zsplit"}, optional. Default is "wilcox".\n        "pratt":\n            includes zero-differences in the ranking process,\n            but drops the ranks of the zeros, see [4]_, (more conservative)\n        "wilcox":\n            discards all zero-differences, the default\n        "zsplit":\n            includes zero-differences in the ranking process and split the\n            zero rank between positive and negative ones\n    correction : bool, optional\n        If True, apply continuity correction by adjusting the Wilcoxon rank\n        statistic by 0.5 towards the mean value when computing the\n        z-statistic.  Default is False.\n    alternative : {"two-sided", "greater", "less"}, optional\n        The alternative hypothesis to be tested, see Notes. Default is\n        "two-sided".\n\n    Returns\n    -------\n    statistic : float\n        If `alternative` is "two-sided", the sum of the ranks of the\n        differences above or below zero, whichever is smaller.\n        Otherwise the sum of the ranks of the differences above zero.\n    pvalue : float\n        The p-value for the test depending on `alternative`.\n\n    See Also\n    --------\n    kruskal, mannwhitneyu\n\n    Notes\n    -----\n    The test has been introduced in [4]_. Given n independent samples\n    (xi, yi) from a bivariate distribution (i.e. paired samples),\n    it computes the differences di = xi - yi. One assumption of the test\n    is that the differences are symmetric, see [2]_.\n    The two-sided test has the null hypothesis that the median of the\n    differences is zero against the alternative that it is different from\n    zero. The one-sided test has the null hypothesis that the median is \n    positive against the alternative that it is negative \n    (``alternative == \'less\'``), or vice versa (``alternative == \'greater.\'``).\n\n    The test uses a normal approximation to derive the p-value (if\n    ``zero_method == \'pratt\'``, the approximation is adjusted as in [5]_).\n    A typical rule is to require that n > 20 ([2]_, p. 383). For smaller n,\n    exact tables can be used to find critical values.\n\n    References\n    ----------\n    .. [1] https://en.wikipedia.org/wiki/Wilcoxon_signed-rank_test\n    .. [2] Conover, W.J., Practical Nonparametric Statistics, 1971.\n    .. [3] Pratt, J.W., Remarks on Zeros and Ties in the Wilcoxon Signed\n       Rank Procedures, Journal of the American Statistical Association,\n       Vol. 54, 1959, pp. 655-667. :doi:`10.1080/01621459.1959.10501526`\n    .. [4] Wilcoxon, F., Individual Comparisons by Ranking Methods,\n       Biometrics Bulletin, Vol. 1, 1945, pp. 80-83. :doi:`10.2307/3001968`\n    .. [5] Cureton, E.E., The Normal Approximation to the Signed-Rank\n       Sampling Distribution When Zero Differences are Present,\n       Journal of the American Statistical Association, Vol. 62, 1967,\n       pp. 1068-1069. :doi:`10.1080/01621459.1967.10500917`\n\n    Examples\n    --------\n    In [4]_, the differences in height between cross- and self-fertilized\n    corn plants is given as follows:\n\n    >>> d = [6, 8, 14, 16, 23, 24, 28, 29, 41, -48, 49, 56, 60, -67, 75]\n\n    Cross-fertilized plants appear to be be higher. To test the null\n    hypothesis that there is no height difference, we can apply the\n    two-sided test:\n\n    >>> from scipy.stats import wilcoxon\n    >>> w, p = wilcoxon(d)\n    >>> w, p\n    (24.0, 0.04088813291185591)\n\n    Hence, we would reject the null hypothesis at a confidence level of 5%,\n    concluding that there is a difference in height between the groups.\n    To confirm that the median of the differences can be assumed to be\n    positive, we use:\n\n    >>> w, p = wilcoxon(d, alternative=\'greater\')\n    >>> w, p\n    (96.0, 0.020444066455927955)\n\n    This shows that the null hypothesis that the median is negative can be\n    rejected at a confidence level of 5% in favor of the alternative that\n    the median is greater than zero. The p-value based on the approximation\n    is within the range of 0.019 and 0.054 given in [2]_.\n    Note that the statistic changed to 96 in the one-sided case (the sum\n    of ranks of positive differences) whereas it is 24 in the two-sided\n    case (the minimum of sum of ranks above and below zero).\n\n    '
    if (zero_method not in ['wilcox', 'pratt', 'zsplit']):
        raise ValueError("Zero method should be either 'wilcox' or 'pratt' or 'zsplit'")
    if (alternative not in ['two-sided', 'less', 'greater']):
        raise ValueError("Alternative must be either 'two-sided', 'greater' or 'less'")
    if (y is None):
        d = asarray(x)
        if (d.ndim > 1):
            raise ValueError('Sample x must be one-dimensional.')
    else:
        (x, y) = map(asarray, (x, y))
        if ((x.ndim > 1) or (y.ndim > 1)):
            raise ValueError('Samples x and y must be one-dimensional.')
        if (len(x) != len(y)):
            raise ValueError('The samples x and y must have the same length.')
        d = (x - y)
    if (zero_method in ['wilcox', 'pratt']):
        n_zero = np.sum((d == 0), axis=0)
        if (n_zero == len(d)):
            raise ValueError("zero_method 'wilcox' and 'pratt' do not work if the x - y is zero for all elements.")
    if (zero_method == 'wilcox'):
        d = compress(np.not_equal(d, 0), d, axis=(- 1))
    count = len(d)
    if (count < 10):
        warnings.warn('Sample size too small for normal approximation.')
    r = stats.rankdata(abs(d))
    r_plus = np.sum(((d > 0) * r), axis=0)
    r_minus = np.sum(((d < 0) * r), axis=0)
    if (zero_method == 'zsplit'):
        r_zero = np.sum(((d == 0) * r), axis=0)
        r_plus += (r_zero / 2.0)
        r_minus += (r_zero / 2.0)
    if (alternative == 'two-sided'):
        T = min(r_plus, r_minus)
    else:
        T = r_plus
    mn = ((count * (count + 1.0)) * 0.25)
    se = ((count * (count + 1.0)) * ((2.0 * count) + 1.0))
    if (zero_method == 'pratt'):
        r = r[(d != 0)]
        mn -= ((n_zero * (n_zero + 1.0)) * 0.25)
        se -= ((n_zero * (n_zero + 1.0)) * ((2.0 * n_zero) + 1.0))
    (replist, repnum) = find_repeats(r)
    if (repnum.size != 0):
        se -= (0.5 * (repnum * ((repnum * repnum) - 1)).sum())
    se = sqrt((se / 24))
    d = 0
    if correction:
        if (alternative == 'two-sided'):
            d = (0.5 * np.sign((T - mn)))
        elif (alternative == 'less'):
            d = (- 0.5)
        else:
            d = 0.5
    z = (((T - mn) - d) / se)
    if (alternative == 'two-sided'):
        prob = (2.0 * distributions.norm.sf(abs(z)))
    elif (alternative == 'greater'):
        prob = distributions.norm.sf(z)
    else:
        prob = distributions.norm.cdf(z)
    return WilcoxonResult(T, prob)
