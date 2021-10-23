

def f_oneway(*args):
    '\n    Performs a 1-way ANOVA.\n\n    The one-way ANOVA tests the null hypothesis that two or more groups have\n    the same population mean.  The test is applied to samples from two or\n    more groups, possibly with differing sizes.\n\n    Parameters\n    ----------\n    sample1, sample2, ... : array_like\n        The sample measurements for each group.\n\n    Returns\n    -------\n    statistic : float\n        The computed F-value of the test.\n    pvalue : float\n        The associated p-value from the F-distribution.\n\n    Notes\n    -----\n    The ANOVA test has important assumptions that must be satisfied in order\n    for the associated p-value to be valid.\n\n    1. The samples are independent.\n    2. Each sample is from a normally distributed population.\n    3. The population standard deviations of the groups are all equal.  This\n       property is known as homoscedasticity.\n\n    If these assumptions are not true for a given set of data, it may still be\n    possible to use the Kruskal-Wallis H-test (`scipy.stats.kruskal`) although\n    with some loss of power.\n\n    The algorithm is from Heiman[2], pp.394-7.\n\n\n    References\n    ----------\n    .. [1] Lowry, Richard.  "Concepts and Applications of Inferential\n           Statistics". Chapter 14.\n           https://web.archive.org/web/20171027235250/http://vassarstats.net:80/textbook/ch14pt1.html\n\n    .. [2] Heiman, G.W.  Research Methods in Statistics. 2002.\n\n    .. [3] McDonald, G. H. "Handbook of Biological Statistics", One-way ANOVA.\n           http://www.biostathandbook.com/onewayanova.html\n\n    Examples\n    --------\n    >>> import scipy.stats as stats\n\n    [3]_ Here are some data on a shell measurement (the length of the anterior\n    adductor muscle scar, standardized by dividing by length) in the mussel\n    Mytilus trossulus from five locations: Tillamook, Oregon; Newport, Oregon;\n    Petersburg, Alaska; Magadan, Russia; and Tvarminne, Finland, taken from a\n    much larger data set used in McDonald et al. (1991).\n\n    >>> tillamook = [0.0571, 0.0813, 0.0831, 0.0976, 0.0817, 0.0859, 0.0735,\n    ...              0.0659, 0.0923, 0.0836]\n    >>> newport = [0.0873, 0.0662, 0.0672, 0.0819, 0.0749, 0.0649, 0.0835,\n    ...            0.0725]\n    >>> petersburg = [0.0974, 0.1352, 0.0817, 0.1016, 0.0968, 0.1064, 0.105]\n    >>> magadan = [0.1033, 0.0915, 0.0781, 0.0685, 0.0677, 0.0697, 0.0764,\n    ...            0.0689]\n    >>> tvarminne = [0.0703, 0.1026, 0.0956, 0.0973, 0.1039, 0.1045]\n    >>> stats.f_oneway(tillamook, newport, petersburg, magadan, tvarminne)\n    (7.1210194716424473, 0.00028122423145345439)\n\n    '
    args = [np.asarray(arg, dtype=float) for arg in args]
    num_groups = len(args)
    alldata = np.concatenate(args)
    bign = len(alldata)
    offset = alldata.mean()
    alldata -= offset
    sstot = (_sum_of_squares(alldata) - (_square_of_sums(alldata) / bign))
    ssbn = 0
    for a in args:
        ssbn += (_square_of_sums((a - offset)) / len(a))
    ssbn -= (_square_of_sums(alldata) / bign)
    sswn = (sstot - ssbn)
    dfbn = (num_groups - 1)
    dfwn = (bign - num_groups)
    msb = (ssbn / dfbn)
    msw = (sswn / dfwn)
    f = (msb / msw)
    prob = special.fdtrc(dfbn, dfwn, f)
    return F_onewayResult(f, prob)
