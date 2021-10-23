def _get_missing_features_info(self, X):
    'Compute the imputer mask and the indices of the features\n        containing missing values.\n\n        Parameters\n        ----------\n        X : {ndarray or sparse matrix}, shape (n_samples, n_features)\n            The input data with missing values. Note that ``X`` has been\n            checked in ``fit`` and ``transform`` before to call this function.\n\n        Returns\n        -------\n        imputer_mask : {ndarray or sparse matrix}, shape (n_samples, n_features) or (n_samples, n_features_with_missing)\n            The imputer mask of the original data.\n\n        features_with_missing : ndarray, shape (n_features_with_missing)\n            The features containing missing values.\n\n        '
    if sparse.issparse(X):
        mask = _get_mask(X.data, self.missing_values)
        sparse_constructor = (sparse.csr_matrix if (X.format == 'csr') else sparse.csc_matrix)
        imputer_mask = sparse_constructor((mask, X.indices.copy(), X.indptr.copy()), shape=X.shape, dtype=bool)
        imputer_mask.eliminate_zeros()
        if (self.features == 'missing-only'):
            n_missing = imputer_mask.getnnz(axis=0)
        if (self.sparse is False):
            imputer_mask = imputer_mask.toarray()
        elif (imputer_mask.format == 'csr'):
            imputer_mask = imputer_mask.tocsc()
    else:
        imputer_mask = _get_mask(X, self.missing_values)
        if (self.features == 'missing-only'):
            n_missing = imputer_mask.sum(axis=0)
        if (self.sparse is True):
            imputer_mask = sparse.csc_matrix(imputer_mask)
    if (self.features == 'all'):
        features_indices = np.arange(X.shape[1])
    else:
        features_indices = np.flatnonzero(n_missing)
    return (imputer_mask, features_indices)