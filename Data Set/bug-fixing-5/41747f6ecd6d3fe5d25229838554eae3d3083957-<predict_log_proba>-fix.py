def predict_log_proba(self, X):
    'Predict class log-probabilities of the input samples X.\n\n        Parameters\n        ----------\n        X : {array-like, sparse matrix} of shape (n_samples, n_features)\n            The input samples. Internally, it will be converted to\n            ``dtype=np.float32`` and if a sparse matrix is provided\n            to a sparse ``csr_matrix``.\n\n        Returns\n        -------\n        proba : ndarray of shape (n_samples, n_classes) or list of n_outputs             such arrays if n_outputs > 1\n            The class log-probabilities of the input samples. The order of the\n            classes corresponds to that in the attribute :term:`classes_`.\n        '
    proba = self.predict_proba(X)
    if (self.n_outputs_ == 1):
        return np.log(proba)
    else:
        for k in range(self.n_outputs_):
            proba[k] = np.log(proba[k])
        return proba