@property
def predict_proba(self):
    'Compute probabilities of possible outcomes for samples in X.\n\n        Parameters\n        ----------\n        X : {array-like, sparse matrix}, shape = [n_samples, n_features]\n            Training vectors, where n_samples is the number of samples and\n            n_features is the number of features.\n\n        Returns\n        ----------\n        avg : array-like, shape = [n_samples, n_classes]\n            Weighted average probability for each class per sample.\n        '
    return self._predict_proba