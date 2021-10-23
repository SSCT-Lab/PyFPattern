def score_samples(self, X):
    'Evaluate the density model on the data.\n\n        Parameters\n        ----------\n        X : array_like, shape (n_samples, n_features)\n            An array of points to query.  Last dimension should match dimension\n            of training data (n_features).\n\n        Returns\n        -------\n        density : ndarray, shape (n_samples,)\n            The array of log(density) evaluations. These are normalized to be\n            probability densities, so values will be low for high-dimensional\n            data.\n        '
    X = check_array(X, order='C', dtype=DTYPE)
    if (self.tree_.sample_weight is None):
        N = self.tree_.data.shape[0]
    else:
        N = self.tree_.sum_weight
    atol_N = (self.atol * N)
    log_density = self.tree_.kernel_density(X, h=self.bandwidth, kernel=self.kernel, atol=atol_N, rtol=self.rtol, breadth_first=self.breadth_first, return_log=True)
    log_density -= np.log(N)
    return log_density