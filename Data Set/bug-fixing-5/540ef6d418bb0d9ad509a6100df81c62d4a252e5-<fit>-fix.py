def fit(self, X, y=None):
    'Fit the imputer on X.\n\n        Parameters\n        ----------\n        X : {array-like, sparse matrix}, shape (n_samples, n_features)\n            Input data, where ``n_samples`` is the number of samples and\n            ``n_features`` is the number of features.\n\n        Returns\n        -------\n        self : Imputer\n            Returns self.\n        '
    allowed_strategies = ['mean', 'median', 'most_frequent']
    if (self.strategy not in allowed_strategies):
        raise ValueError('Can only use these strategies: {0}  got strategy={1}'.format(allowed_strategies, self.strategy))
    if (self.axis not in [0, 1]):
        raise ValueError('Can only impute missing values on axis 0 and 1,  got axis={0}'.format(self.axis))
    if (self.axis == 0):
        X = check_array(X, accept_sparse='csc', dtype=np.float64, force_all_finite=False)
        if sparse.issparse(X):
            self.statistics_ = self._sparse_fit(X, self.strategy, self.missing_values, self.axis)
        else:
            self.statistics_ = self._dense_fit(X, self.strategy, self.missing_values, self.axis)
    return self