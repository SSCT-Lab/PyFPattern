def _lognorm_logpdf(x, s):
    return _lazywhere((x != 0), (x, s), (lambda x, s: (((- (np.log(x) ** 2)) / (2 * (s ** 2))) - np.log(((s * x) * np.sqrt((2 * np.pi)))))), (- np.inf))