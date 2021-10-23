def predict(self, X, check_input=True):
    "Predict class or regression value for X.\n\n        For a classification model, the predicted class for each sample in X is\n        returned. For a regression model, the predicted value based on X is\n        returned.\n\n        Parameters\n        ----------\n        X : {array-like, sparse matrix} of shape (n_samples, n_features)\n            The input samples. Internally, it will be converted to\n            ``dtype=np.float32`` and if a sparse matrix is provided\n            to a sparse ``csr_matrix``.\n\n        check_input : bool, default=True\n            Allow to bypass several input checking.\n            Don't use this parameter unless you know what you do.\n\n        Returns\n        -------\n        y : array-like of shape (n_samples,) or (n_samples, n_outputs)\n            The predicted classes, or the predict values.\n        "
    check_is_fitted(self)
    X = self._validate_X_predict(X, check_input)
    proba = self.tree_.predict(X)
    n_samples = X.shape[0]
    if is_classifier(self):
        if (self.n_outputs_ == 1):
            return self.classes_.take(np.argmax(proba, axis=1), axis=0)
        else:
            class_type = self.classes_[0].dtype
            predictions = np.zeros((n_samples, self.n_outputs_), dtype=class_type)
            for k in range(self.n_outputs_):
                predictions[:, k] = self.classes_[k].take(np.argmax(proba[:, k], axis=1), axis=0)
            return predictions
    elif (self.n_outputs_ == 1):
        return proba[:, 0]
    else:
        return proba[:, :, 0]