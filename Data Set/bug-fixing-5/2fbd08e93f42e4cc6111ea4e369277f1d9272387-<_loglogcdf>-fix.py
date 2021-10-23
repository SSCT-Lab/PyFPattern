def _loglogcdf(self, x, c):
    return _lazywhere(((x == x) & (c != 0)), (x, c), (lambda x, c: (sc.log1p(((- c) * x)) / c)), (- x))