def predict(self, X):
    'Predict using the linear model\n\n        Parameters\n        ----------\n        X : {array-like, sparse matrix}, shape (n_samples, n_features)\n\n        Returns\n        -------\n        array, shape (n_samples,)\n           Predicted target values per element in X.\n        '
    return self._decision_function(X)