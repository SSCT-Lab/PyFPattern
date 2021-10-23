@property
def predict_proba(self):
    'Compute probabilities of possible outcomes for samples in X.\n\n        Parameters\n        ----------\n        X : {array-like, sparse matrix}, shape = [n_samples, n_features]\n            The input samples.\n\n        Returns\n        ----------\n        avg : array-like, shape = [n_samples, n_classes]\n            Weighted average probability for each class per sample.\n        '
    return self._predict_proba