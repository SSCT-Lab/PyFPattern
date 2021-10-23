def predict(self, X):
    '\n        Perform classification on samples in X.\n\n        For a one-class model, +1 or -1 is returned.\n\n        Parameters\n        ----------\n        X : {array-like, sparse matrix}, shape (n_samples, n_features)\n            For kernel="precomputed", the expected shape of X is\n            [n_samples_test, n_samples_train]\n\n        Returns\n        -------\n        y_pred : array, shape (n_samples,)\n            Class labels for samples in X.\n        '
    y = super().predict(X)
    return np.asarray(y, dtype=np.intp)