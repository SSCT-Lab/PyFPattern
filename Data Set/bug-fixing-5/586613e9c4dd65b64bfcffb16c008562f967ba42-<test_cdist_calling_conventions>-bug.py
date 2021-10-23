def test_cdist_calling_conventions(self):
    for eo_name in self.rnd_eo_names:
        X1 = eo[eo_name][:, ::(- 1)]
        X2 = eo[eo_name][:(- 3):2]
        for metric in _metrics:
            if (verbose > 2):
                print('testing: ', metric, ' with: ', eo_name)
            if ((metric == 'yule') and ('bool' not in eo_name)):
                continue
            self._check_calling_conventions(X1, X2, metric)
            if (metric == 'wminkowski'):
                w = (1.0 / X1.std(axis=0))
                self._check_calling_conventions(X1, X2, metric, w=w)
            elif (metric == 'seuclidean'):
                X12 = np.vstack([X1, X2]).astype(np.double)
                V = np.var(X12, axis=0, ddof=1)
                self._check_calling_conventions(X1, X2, metric, V=V)
            elif (metric == 'mahalanobis'):
                X12 = np.vstack([X1, X2]).astype(np.double)
                V = np.atleast_2d(np.cov(X12.T))
                VI = np.array(np.linalg.inv(V).T)
                self._check_calling_conventions(X1, X2, metric, VI=VI)