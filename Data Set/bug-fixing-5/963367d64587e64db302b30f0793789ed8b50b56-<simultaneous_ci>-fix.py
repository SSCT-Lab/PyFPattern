def simultaneous_ci(q_crit, var, groupnobs, pairindices=None):
    "Compute simultaneous confidence intervals for comparison of means.\n\n    q_crit value is generated from tukey hsd test. Variance is considered\n    across all groups. Returned halfwidths can be thought of as uncertainty\n    intervals around each group mean. They allow for simultaneous\n    comparison of pairwise significance among any pairs (by checking for\n    overlap)\n\n    Parameters\n    ----------\n    q_crit : float\n        The Q critical value studentized range statistic from Tukey's HSD\n    var : float\n        The group variance\n    groupnobs : array-like object\n        Number of observations contained in each group.\n    pairindices : tuple of lists, optional\n        Indices corresponding to the upper triangle of matrix. Computed\n        here if not supplied\n\n    Returns\n    -------\n    halfwidths : ndarray\n        Half the width of each confidence interval for each group given in\n        groupnobs\n\n    See Also\n    --------\n    MultiComparison : statistics class providing significance tests\n    tukeyhsd : among other things, computes q_crit value\n\n    References\n    ----------\n    .. [1] Hochberg, Y., and A. C. Tamhane. Multiple Comparison Procedures.\n           Hoboken, NJ: John Wiley & Sons, 1987.)\n    "
    ng = len(groupnobs)
    if (pairindices is None):
        pairindices = np.triu_indices(ng, 1)
    gvar = (var / groupnobs)
    d12 = np.sqrt((gvar[pairindices[0]] + gvar[pairindices[1]]))
    d = np.zeros((ng, ng))
    d[pairindices] = d12
    d = (d + d.conj().T)
    sum1 = np.sum(d12)
    sum2 = np.sum(d, axis=0)
    if (ng > 2):
        w = ((((ng - 1.0) * sum2) - sum1) / ((ng - 1.0) * (ng - 2.0)))
    else:
        w = ((sum1 * np.ones((2, 1))) / 2.0)
    return ((q_crit / np.sqrt(2)) * w)