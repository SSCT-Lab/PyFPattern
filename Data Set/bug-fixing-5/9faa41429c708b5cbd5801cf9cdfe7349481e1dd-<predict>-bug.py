def predict(self, X):
    ' Predict class labels for X.\n\n        Parameters\n        ----------\n        X : {array-like, sparse matrix}, shape = [n_samples, n_features]\n            Training vectors, where n_samples is the number of samples and\n            n_features is the number of features.\n\n        Returns\n        ----------\n        maj : array-like, shape = [n_samples]\n            Predicted class labels.\n        '
    check_is_fitted(self, 'estimators_')
    if (self.voting == 'soft'):
        maj = np.argmax(self.predict_proba(X), axis=1)
    else:
        predictions = self._predict(X)
        maj = np.apply_along_axis((lambda x: np.argmax(np.bincount(x, weights=self._weights_not_none))), axis=1, arr=predictions)
    maj = self.le_.inverse_transform(maj)
    return maj