def test_pdist_calling_conventions(self):
    eps = 1e-07
    for eo_name in self.rnd_eo_names:
        X = eo[eo_name][::2]
        for metric in _metrics:
            if (verbose > 2):
                print('testing: ', metric, ' with: ', eo_name)
            if ((metric == 'yule') and ('bool' not in eo_name)):
                continue
            self._check_calling_conventions(X, metric)
            if (metric == 'wminkowski'):
                w = (1.0 / X.std(axis=0))
                self._check_calling_conventions(X, metric, w=w)
            elif (metric == 'seuclidean'):
                V = np.var(X.astype(np.double), axis=0, ddof=1)
                self._check_calling_conventions(X, metric, V=V)
            elif (metric == 'mahalanobis'):
                V = np.atleast_2d(np.cov(X.astype(np.double).T))
                VI = np.array(np.linalg.inv(V).T)
                self._check_calling_conventions(X, metric, VI=VI)