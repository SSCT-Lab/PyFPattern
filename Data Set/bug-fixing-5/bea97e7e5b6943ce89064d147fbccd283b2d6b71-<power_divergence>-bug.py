def power_divergence(f_obs, f_exp=None, ddof=0, axis=0, lambda_=None):
    '\n    Cressie-Read power divergence statistic and goodness of fit test.\n\n    This function tests the null hypothesis that the categorical data\n    has the given frequencies, using the Cressie-Read power divergence\n    statistic.\n\n    Parameters\n    ----------\n    f_obs : array_like\n        Observed frequencies in each category.\n    f_exp : array_like, optional\n        Expected frequencies in each category.  By default the categories are\n        assumed to be equally likely.\n    ddof : int, optional\n        "Delta degrees of freedom": adjustment to the degrees of freedom\n        for the p-value.  The p-value is computed using a chi-squared\n        distribution with ``k - 1 - ddof`` degrees of freedom, where `k`\n        is the number of observed frequencies.  The default value of `ddof`\n        is 0.\n    axis : int or None, optional\n        The axis of the broadcast result of `f_obs` and `f_exp` along which to\n        apply the test.  If axis is None, all values in `f_obs` are treated\n        as a single data set.  Default is 0.\n    lambda_ : float or str, optional\n        `lambda_` gives the power in the Cressie-Read power divergence\n        statistic.  The default is 1.  For convenience, `lambda_` may be\n        assigned one of the following strings, in which case the\n        corresponding numerical value is used::\n\n            String              Value   Description\n            "pearson"             1     Pearson\'s chi-squared statistic.\n                                        In this case, the function is\n                                        equivalent to `stats.chisquare`.\n            "log-likelihood"      0     Log-likelihood ratio. Also known as\n                                        the G-test [3]_.\n            "freeman-tukey"      -1/2   Freeman-Tukey statistic.\n            "mod-log-likelihood" -1     Modified log-likelihood ratio.\n            "neyman"             -2     Neyman\'s statistic.\n            "cressie-read"        2/3   The power recommended in [5]_.\n\n    Returns\n    -------\n    statistic : float or ndarray\n        The Cressie-Read power divergence test statistic.  The value is\n        a float if `axis` is None or if` `f_obs` and `f_exp` are 1-D.\n    pvalue : float or ndarray\n        The p-value of the test.  The value is a float if `ddof` and the\n        return value `stat` are scalars.\n\n    See Also\n    --------\n    chisquare\n\n    Notes\n    -----\n    This test is invalid when the observed or expected frequencies in each\n    category are too small.  A typical rule is that all of the observed\n    and expected frequencies should be at least 5.\n\n    When `lambda_` is less than zero, the formula for the statistic involves\n    dividing by `f_obs`, so a warning or error may be generated if any value\n    in `f_obs` is 0.\n\n    Similarly, a warning or error may be generated if any value in `f_exp` is\n    zero when `lambda_` >= 0.\n\n    The default degrees of freedom, k-1, are for the case when no parameters\n    of the distribution are estimated. If p parameters are estimated by\n    efficient maximum likelihood then the correct degrees of freedom are\n    k-1-p. If the parameters are estimated in a different way, then the\n    dof can be between k-1-p and k-1. However, it is also possible that\n    the asymptotic distribution is not a chisquare, in which case this\n    test is not appropriate.\n\n    This function handles masked arrays.  If an element of `f_obs` or `f_exp`\n    is masked, then data at that position is ignored, and does not count\n    towards the size of the data set.\n\n    .. versionadded:: 0.13.0\n\n    References\n    ----------\n    .. [1] Lowry, Richard.  "Concepts and Applications of Inferential\n           Statistics". Chapter 8.\n           https://web.archive.org/web/20171015035606/http://faculty.vassar.edu/lowry/ch8pt1.html\n    .. [2] "Chi-squared test", https://en.wikipedia.org/wiki/Chi-squared_test\n    .. [3] "G-test", https://en.wikipedia.org/wiki/G-test\n    .. [4] Sokal, R. R. and Rohlf, F. J. "Biometry: the principles and\n           practice of statistics in biological research", New York: Freeman\n           (1981)\n    .. [5] Cressie, N. and Read, T. R. C., "Multinomial Goodness-of-Fit\n           Tests", J. Royal Stat. Soc. Series B, Vol. 46, No. 3 (1984),\n           pp. 440-464.\n\n    Examples\n    --------\n\n    (See `chisquare` for more examples.)\n\n    When just `f_obs` is given, it is assumed that the expected frequencies\n    are uniform and given by the mean of the observed frequencies.  Here we\n    perform a G-test (i.e. use the log-likelihood ratio statistic):\n\n    >>> from scipy.stats import power_divergence\n    >>> power_divergence([16, 18, 16, 14, 12, 12], lambda_=\'log-likelihood\')\n    (2.006573162632538, 0.84823476779463769)\n\n    The expected frequencies can be given with the `f_exp` argument:\n\n    >>> power_divergence([16, 18, 16, 14, 12, 12],\n    ...                  f_exp=[16, 16, 16, 16, 16, 8],\n    ...                  lambda_=\'log-likelihood\')\n    (3.3281031458963746, 0.6495419288047497)\n\n    When `f_obs` is 2-D, by default the test is applied to each column.\n\n    >>> obs = np.array([[16, 18, 16, 14, 12, 12], [32, 24, 16, 28, 20, 24]]).T\n    >>> obs.shape\n    (6, 2)\n    >>> power_divergence(obs, lambda_="log-likelihood")\n    (array([ 2.00657316,  6.77634498]), array([ 0.84823477,  0.23781225]))\n\n    By setting ``axis=None``, the test is applied to all data in the array,\n    which is equivalent to applying the test to the flattened array.\n\n    >>> power_divergence(obs, axis=None)\n    (23.31034482758621, 0.015975692534127565)\n    >>> power_divergence(obs.ravel())\n    (23.31034482758621, 0.015975692534127565)\n\n    `ddof` is the change to make to the default degrees of freedom.\n\n    >>> power_divergence([16, 18, 16, 14, 12, 12], ddof=1)\n    (2.0, 0.73575888234288467)\n\n    The calculation of the p-values is done by broadcasting the\n    test statistic with `ddof`.\n\n    >>> power_divergence([16, 18, 16, 14, 12, 12], ddof=[0,1,2])\n    (2.0, array([ 0.84914504,  0.73575888,  0.5724067 ]))\n\n    `f_obs` and `f_exp` are also broadcast.  In the following, `f_obs` has\n    shape (6,) and `f_exp` has shape (2, 6), so the result of broadcasting\n    `f_obs` and `f_exp` has shape (2, 6).  To compute the desired chi-squared\n    statistics, we must use ``axis=1``:\n\n    >>> power_divergence([16, 18, 16, 14, 12, 12],\n    ...                  f_exp=[[16, 16, 16, 16, 16, 8],\n    ...                         [8, 20, 20, 16, 12, 12]],\n    ...                  axis=1)\n    (array([ 3.5 ,  9.25]), array([ 0.62338763,  0.09949846]))\n\n    '
    if isinstance(lambda_, string_types):
        if (lambda_ not in _power_div_lambda_names):
            names = repr(list(_power_div_lambda_names.keys()))[1:(- 1)]
            raise ValueError('invalid string for lambda_: {0!r}.  Valid strings are {1}'.format(lambda_, names))
        lambda_ = _power_div_lambda_names[lambda_]
    elif (lambda_ is None):
        lambda_ = 1
    f_obs = np.asanyarray(f_obs)
    if (f_exp is not None):
        f_exp = np.atleast_1d(np.asanyarray(f_exp))
    else:
        with np.errstate(invalid='ignore'):
            f_exp = np.atleast_1d(f_obs.mean(axis=axis))
        if (axis is not None):
            reduced_shape = list(f_obs.shape)
            reduced_shape[axis] = 1
            f_exp.shape = reduced_shape
    if (lambda_ == 1):
        terms = (((f_obs - f_exp) ** 2) / f_exp)
    elif (lambda_ == 0):
        terms = (2.0 * special.xlogy(f_obs, (f_obs / f_exp)))
    elif (lambda_ == (- 1)):
        terms = (2.0 * special.xlogy(f_exp, (f_exp / f_obs)))
    else:
        terms = (f_obs * (((f_obs / f_exp) ** lambda_) - 1))
        terms /= ((0.5 * lambda_) * (lambda_ + 1))
    stat = terms.sum(axis=axis)
    num_obs = _count(terms, axis=axis)
    ddof = asarray(ddof)
    p = distributions.chi2.sf(stat, ((num_obs - 1) - ddof))
    return Power_divergenceResult(stat, p)