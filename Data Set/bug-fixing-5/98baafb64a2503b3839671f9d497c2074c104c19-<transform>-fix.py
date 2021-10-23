def transform(self, X):
    'Transform dataset.\n\n        Parameters\n        ----------\n        X : array-like or sparse matrix, shape=(n_samples, n_features)\n            Input data to be transformed. Use ``dtype=np.float32`` for maximum\n            efficiency. Sparse matrices are also supported, use sparse\n            ``csr_matrix`` for maximum efficiency.\n\n        Returns\n        -------\n        X_transformed : sparse matrix, shape=(n_samples, n_out)\n            Transformed dataset.\n        '
    check_is_fitted(self, 'one_hot_encoder_')
    return self.one_hot_encoder_.transform(self.apply(X))