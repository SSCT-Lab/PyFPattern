def predict_proba(self, X, check_input=True):
    "Predict class probabilities of the input samples X.\n\n        The predicted class probability is the fraction of samples of the same\n        class in a leaf.\n\n        check_input : boolean, (default=True)\n            Allow to bypass several input checking.\n            Don't use this parameter unless you know what you do.\n\n        Parameters\n        ----------\n        X : array-like or sparse matrix of shape (n_samples, n_features)\n            The input samples. Internally, it will be converted to\n            ``dtype=np.float32`` and if a sparse matrix is provided\n            to a sparse ``csr_matrix``.\n\n        check_input : bool\n            Run check_array on X.\n\n        Returns\n        -------\n        proba : array of shape (n_samples, n_classes), or a list of n_outputs             such arrays if n_outputs > 1.\n            The class probabilities of the input samples. The order of the\n            classes corresponds to that in the attribute :term:`classes_`.\n        "
    check_is_fitted(self)
    X = self._validate_X_predict(X, check_input)
    proba = self.tree_.predict(X)
    if (self.n_outputs_ == 1):
        proba = proba[:, :self.n_classes_]
        normalizer = proba.sum(axis=1)[:, np.newaxis]
        normalizer[(normalizer == 0.0)] = 1.0
        proba /= normalizer
        return proba
    else:
        all_proba = []
        for k in range(self.n_outputs_):
            proba_k = proba[:, k, :self.n_classes_[k]]
            normalizer = proba_k.sum(axis=1)[:, np.newaxis]
            normalizer[(normalizer == 0.0)] = 1.0
            proba_k /= normalizer
            all_proba.append(proba_k)
        return all_proba