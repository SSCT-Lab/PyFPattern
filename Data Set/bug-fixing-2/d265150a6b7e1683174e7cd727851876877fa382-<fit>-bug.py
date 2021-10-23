

def fit(self, q=0.5, vcov='robust', kernel='epa', bandwidth='hsheather', max_iter=1000, p_tol=1e-06, **kwargs):
    'Solve by Iterative Weighted Least Squares\n\n        Parameters\n        ----------\n        q : float\n            Quantile must be between 0 and 1\n        vcov : string, method used to calculate the variance-covariance matrix\n            of the parameters. Default is ``robust``:\n\n            - robust : heteroskedasticity robust standard errors (as suggested\n              in Greene 6th edition)\n            - iid : iid errors (as in Stata 12)\n\n        kernel : string, kernel to use in the kernel density estimation for the\n            asymptotic covariance matrix:\n\n            - epa: Epanechnikov\n            - cos: Cosine\n            - gau: Gaussian\n            - par: Parzene\n\n        bandwidth: string, Bandwidth selection method in kernel density\n            estimation for asymptotic covariance estimate (full\n            references in QuantReg docstring):\n\n            - hsheather: Hall-Sheather (1988)\n            - bofinger: Bofinger (1975)\n            - chamberlain: Chamberlain (1994)\n        '
    if ((q < 0) or (q > 1)):
        raise Exception('p must be between 0 and 1')
    kern_names = ['biw', 'cos', 'epa', 'gau', 'par']
    if (kernel not in kern_names):
        raise Exception(('kernel must be one of ' + ', '.join(kern_names)))
    else:
        kernel = kernels[kernel]
    if (bandwidth == 'hsheather'):
        bandwidth = hall_sheather
    elif (bandwidth == 'bofinger'):
        bandwidth = bofinger
    elif (bandwidth == 'chamberlain'):
        bandwidth = chamberlain
    else:
        raise Exception("bandwidth must be in 'hsheather', 'bofinger', 'chamberlain'")
    endog = self.endog
    exog = self.exog
    nobs = self.nobs
    exog_rank = np_matrix_rank(self.exog)
    self.rank = exog_rank
    self.df_model = float((self.rank - self.k_constant))
    self.df_resid = (self.nobs - self.rank)
    n_iter = 0
    xstar = exog
    beta = np.ones(exog_rank)
    diff = 10
    cycle = False
    history = dict(params=[], mse=[])
    while ((n_iter < max_iter) and (diff > p_tol) and (not cycle)):
        n_iter += 1
        beta0 = beta
        xtx = np.dot(xstar.T, exog)
        xty = np.dot(xstar.T, endog)
        beta = np.dot(pinv(xtx), xty)
        resid = (endog - np.dot(exog, beta))
        mask = (np.abs(resid) < 1e-06)
        resid[mask] = ((((resid[mask] >= 0) * 2) - 1) * 1e-06)
        resid = np.where((resid < 0), (q * resid), ((1 - q) * resid))
        resid = np.abs(resid)
        xstar = (exog / resid[:, np.newaxis])
        diff = np.max(np.abs((beta - beta0)))
        history['params'].append(beta)
        history['mse'].append(np.mean((resid * resid)))
        if ((n_iter >= 300) and ((n_iter % 100) == 0)):
            for ii in range(2, 10):
                if np.all((beta == history['params'][(- ii)])):
                    cycle = True
                    break
            warnings.warn('Convergence cycle detected', ConvergenceWarning)
    if (n_iter == max_iter):
        warnings.warn((('Maximum number of iterations (' + str(max_iter)) + ') reached.'), IterationLimitWarning)
    e = (endog - np.dot(exog, beta))
    iqre = (stats.scoreatpercentile(e, 75) - stats.scoreatpercentile(e, 25))
    h = bandwidth(nobs, q)
    h = (min(np.std(endog), (iqre / 1.34)) * (norm.ppf((q + h)) - norm.ppf((q - h))))
    fhat0 = ((1.0 / (nobs * h)) * np.sum(kernel((e / h))))
    if (vcov == 'robust'):
        d = np.where((e > 0), ((q / fhat0) ** 2), (((1 - q) / fhat0) ** 2))
        xtxi = pinv(np.dot(exog.T, exog))
        xtdx = np.dot((exog.T * d[np.newaxis, :]), exog)
        vcov = chain_dot(xtxi, xtdx, xtxi)
    elif (vcov == 'iid'):
        vcov = (((((1.0 / fhat0) ** 2) * q) * (1 - q)) * pinv(np.dot(exog.T, exog)))
    else:
        raise Exception("vcov must be 'robust' or 'iid'")
    lfit = QuantRegResults(self, beta, normalized_cov_params=vcov)
    lfit.q = q
    lfit.iterations = n_iter
    lfit.sparsity = (1.0 / fhat0)
    lfit.bandwidth = h
    lfit.history = history
    return RegressionResultsWrapper(lfit)
