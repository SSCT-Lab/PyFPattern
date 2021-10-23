def _lognorm_logpdf(x, s):
    return _lazywhere((x != 0), (x, s), (lambda x, s: (((- (log(x) ** 2)) / (2 * (s ** 2))) - log(((s * x) * sqrt((2 * pi)))))), (- np.inf))