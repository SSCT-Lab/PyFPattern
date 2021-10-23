def _decision_function(self, X):
    'Predict using the linear model\n\n        Parameters\n        ----------\n        X : {array-like, sparse matrix}, shape (n_samples, n_features)\n\n        Returns\n        -------\n        array, shape (n_samples,)\n           Predicted target values per element in X.\n        '
    check_is_fitted(self)
    X = check_array(X, accept_sparse='csr')
    scores = (safe_sparse_dot(X, self.coef_.T, dense_output=True) + self.intercept_)
    return scores.ravel()