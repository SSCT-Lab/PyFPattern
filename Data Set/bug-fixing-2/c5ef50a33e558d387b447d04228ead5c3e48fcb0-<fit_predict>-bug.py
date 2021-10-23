

def fit_predict(self, X, y=None):
    'Compute cluster centers and predict cluster index for each sample.\n\n        Convenience method; equivalent to calling fit(X) followed by\n        predict(X).\n\n        Parameters\n        ----------\n        X : {array-like, sparse matrix}, shape = [n_samples, n_features]\n            New data to transform.\n\n        u : Ignored\n\n        Returns\n        -------\n        labels : array, shape [n_samples,]\n            Index of the cluster each sample belongs to.\n        '
    return self.fit(X).labels_
