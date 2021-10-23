def _legacy_fit_transform(self, X):
    'Assumes X contains only categorical features.'
    dtype = getattr(X, 'dtype', None)
    X = check_array(X, dtype=np.int)
    if np.any((X < 0)):
        raise ValueError("OneHotEncoder in legacy mode cannot handle categories encoded as negative integers. Please set categories='auto' explicitly to be able to use arbitrary integer values as category identifiers.")
    (n_samples, n_features) = X.shape
    if (isinstance(self.n_values, six.string_types) and (self.n_values == 'auto')):
        n_values = (np.max(X, axis=0) + 1)
    elif isinstance(self.n_values, numbers.Integral):
        if (np.max(X, axis=0) >= self.n_values).any():
            raise ValueError(('Feature out of bounds for n_values=%d' % self.n_values))
        n_values = np.empty(n_features, dtype=np.int)
        n_values.fill(self.n_values)
    else:
        try:
            n_values = np.asarray(self.n_values, dtype=int)
        except (ValueError, TypeError):
            raise TypeError(("Wrong type for parameter `n_values`. Expected 'auto', int or array of ints, got %r" % type(X)))
        if ((n_values.ndim < 1) or (n_values.shape[0] != X.shape[1])):
            raise ValueError('Shape mismatch: if n_values is an array, it has to be of shape (n_features,).')
    self._n_values_ = n_values
    self.categories_ = [np.arange((n_val - 1), dtype=dtype) for n_val in n_values]
    n_values = np.hstack([[0], n_values])
    indices = np.cumsum(n_values)
    self._feature_indices_ = indices
    column_indices = (X + indices[:(- 1)]).ravel()
    row_indices = np.repeat(np.arange(n_samples, dtype=np.int32), n_features)
    data = np.ones((n_samples * n_features))
    out = sparse.coo_matrix((data, (row_indices, column_indices)), shape=(n_samples, indices[(- 1)]), dtype=self.dtype).tocsr()
    if (isinstance(self.n_values, six.string_types) and (self.n_values == 'auto')):
        mask = (np.array(out.sum(axis=0)).ravel() != 0)
        active_features = np.where(mask)[0]
        out = out[:, active_features]
        self._active_features_ = active_features
        self.categories_ = [(np.unique(X[:, i]).astype(dtype) if dtype else np.unique(X[:, i])) for i in range(n_features)]
    return (out if self.sparse else out.toarray())