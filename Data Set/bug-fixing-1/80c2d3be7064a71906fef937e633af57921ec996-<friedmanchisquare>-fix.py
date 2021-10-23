

def friedmanchisquare(*args):
    'Friedman Chi-Square is a non-parametric, one-way within-subjects ANOVA.\n    This function calculates the Friedman Chi-square test for repeated measures\n    and returns the result, along with the associated probability value.\n\n    Each input is considered a given group. Ideally, the number of treatments\n    among each group should be equal. If this is not the case, only the first\n    n treatments are taken into account, where n is the number of treatments\n    of the smallest group.\n    If a group has some missing values, the corresponding treatments are masked\n    in the other groups.\n    The test statistic is corrected for ties.\n\n    Masked values in one group are propagated to the other groups.\n\n    Returns\n    -------\n    statistic : float\n        the test statistic.\n    pvalue : float\n        the associated p-value.\n\n    '
    data = argstoarray(*args).astype(float)
    k = len(data)
    if (k < 3):
        raise ValueError((('Less than 3 groups (%i): ' % k) + 'the Friedman test is NOT appropriate.'))
    ranked = ma.masked_values(rankdata(data, axis=0), 0)
    if (ranked._mask is not nomask):
        ranked = ma.mask_cols(ranked)
        ranked = ranked.compressed().reshape(k, (- 1)).view(ndarray)
    else:
        ranked = ranked._data
    (k, n) = ranked.shape
    repeats = [find_repeats(row) for row in ranked.T]
    ties = np.array([y for (x, y) in repeats if (x.size > 0)])
    tie_correction = (1 - (((ties ** 3) - ties).sum() / float((n * ((k ** 3) - k)))))
    ssbg = np.sum(((ranked.sum((- 1)) - ((n * (k + 1)) / 2.0)) ** 2))
    chisq = ((((ssbg * 12.0) / ((n * k) * (k + 1))) * 1.0) / tie_correction)
    return FriedmanchisquareResult(chisq, distributions.chi2.sf(chisq, (k - 1)))
