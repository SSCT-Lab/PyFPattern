def _legacy_transform(self, X):
    'Assumes X contains only categorical features.'
    X = check_array(X, dtype=np.int)
    if np.any((X < 0)):
        raise ValueError("OneHotEncoder in legacy mode cannot handle categories encoded as negative integers. Please set categories='auto' explicitly to be able to use arbitrary integer values as category identifiers.")
    (n_samples, n_features) = X.shape
    indices = self._feature_indices_
    if (n_features != (indices.shape[0] - 1)):
        raise ValueError(('X has different shape than during fitting. Expected %d, got %d.' % ((indices.shape[0] - 1), n_features)))
    mask = (X < self._n_values_).ravel()
    if np.any((~ mask)):
        if (self.handle_unknown not in ['error', 'ignore']):
            raise ValueError(('handle_unknown should be either error or unknown got %s' % self.handle_unknown))
        if (self.handle_unknown == 'error'):
            raise ValueError(('unknown categorical feature present %s during transform.' % X.ravel()[(~ mask)]))
    column_indices = (X + indices[:(- 1)]).ravel()[mask]
    row_indices = np.repeat(np.arange(n_samples, dtype=np.int32), n_features)[mask]
    data = np.ones(np.sum(mask))
    out = sparse.coo_matrix((data, (row_indices, column_indices)), shape=(n_samples, indices[(- 1)]), dtype=self.dtype).tocsr()
    if (isinstance(self.n_values, six.string_types) and (self.n_values == 'auto')):
        out = out[:, self._active_features_]
    return (out if self.sparse else out.toarray())