

def transform(self, X):
    'Impute all missing values in X.\n\n        Parameters\n        ----------\n        X : {array-like, sparse matrix}, shape = [n_samples, n_features]\n            The input data to complete.\n        '
    if (self.axis == 0):
        check_is_fitted(self, 'statistics_')
        X = check_array(X, accept_sparse='csc', dtype=FLOAT_DTYPES, force_all_finite=False, copy=self.copy)
        statistics = self.statistics_
        if (X.shape[1] != statistics.shape[0]):
            raise ValueError(('X has %d features per sample, expected %d' % (X.shape[1], self.statistics_.shape[0])))
    else:
        X = check_array(X, accept_sparse='csr', dtype=FLOAT_DTYPES, force_all_finite=False, copy=self.copy)
        if sparse.issparse(X):
            statistics = self._sparse_fit(X, self.strategy, self.missing_values, self.axis)
        else:
            statistics = self._dense_fit(X, self.strategy, self.missing_values, self.axis)
    invalid_mask = np.isnan(statistics)
    valid_mask = np.logical_not(invalid_mask)
    valid_statistics = statistics[valid_mask]
    valid_statistics_indexes = np.where(valid_mask)[0]
    missing = np.arange(X.shape[(not self.axis)])[invalid_mask]
    if ((self.axis == 0) and invalid_mask.any()):
        if self.verbose:
            warnings.warn(('Deleting features without observed values: %s' % missing))
        X = X[:, valid_statistics_indexes]
    elif ((self.axis == 1) and invalid_mask.any()):
        raise ValueError(('Some rows only contain missing values: %s' % missing))
    if (sparse.issparse(X) and (self.missing_values != 0)):
        mask = _get_mask(X.data, self.missing_values)
        indexes = np.repeat(np.arange((len(X.indptr) - 1), dtype=np.int), np.diff(X.indptr))[mask]
        X.data[mask] = astype(valid_statistics[indexes], X.dtype, copy=False)
    else:
        if sparse.issparse(X):
            X = X.toarray()
        mask = _get_mask(X, self.missing_values)
        n_missing = np.sum(mask, axis=self.axis)
        values = np.repeat(valid_statistics, n_missing)
        if (self.axis == 0):
            coordinates = np.where(mask.transpose())[::(- 1)]
        else:
            coordinates = mask
        X[coordinates] = values
    return X
