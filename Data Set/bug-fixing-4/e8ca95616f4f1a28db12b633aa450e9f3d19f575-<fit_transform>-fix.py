def fit_transform(self, X, y=None):
    'Generate missing values indicator for X.\n\n        Parameters\n        ----------\n        X : {array-like, sparse matrix}, shape (n_samples, n_features)\n            The input data to complete.\n\n        Returns\n        -------\n        Xt : {ndarray or sparse matrix}, shape (n_samples, n_features)         or (n_samples, n_features_with_missing)\n            The missing indicator for input data. The data type of ``Xt``\n            will be boolean.\n\n        '
    imputer_mask = self._fit(X, y)
    if (self.features_.size < self._n_features):
        imputer_mask = imputer_mask[:, self.features_]
    return imputer_mask