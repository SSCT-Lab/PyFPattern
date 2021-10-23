

def _nnlf_and_penalty(self, x, args):
    cond0 = (~ self._support_mask(x))
    n_bad = np.count_nonzero(cond0, axis=0)
    if (n_bad > 0):
        x = argsreduce((~ cond0), x)[0]
    logpdf = self._logpdf(x, *args)
    finite_logpdf = np.isfinite(logpdf)
    n_bad += np.sum((~ finite_logpdf), axis=0)
    if (n_bad > 0):
        penalty = ((n_bad * log(_XMAX)) * 100)
        return ((- np.sum(logpdf[finite_logpdf], axis=0)) + penalty)
    return (- np.sum(logpdf, axis=0))
