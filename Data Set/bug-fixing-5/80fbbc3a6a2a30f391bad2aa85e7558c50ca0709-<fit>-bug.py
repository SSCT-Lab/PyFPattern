def fit(self, X, augment=False, rounds=1, seed=None):
    'Required for featurewise_center, featurewise_std_normalization\n        and zca_whitening.\n\n        # Arguments\n            X: Numpy array, the data to fit on.\n            augment: whether to fit on randomly augmented samples\n            rounds: if `augment`,\n                how many augmentation passes to do over the data\n            seed: random seed.\n        '
    if (seed is not None):
        np.random.seed(seed)
    X = np.copy(X)
    if augment:
        aX = np.zeros(tuple(([(rounds * X.shape[0])] + list(X.shape)[1:])))
        for r in range(rounds):
            for i in range(X.shape[0]):
                aX[(i + (r * X.shape[0]))] = self.random_transform(X[i])
        X = aX
    if self.featurewise_center:
        self.mean = np.mean(X, axis=0)
        X -= self.mean
    if self.featurewise_std_normalization:
        self.std = np.std(X, axis=0)
        X /= (self.std + 1e-07)
    if self.zca_whitening:
        flatX = np.reshape(X, (X.shape[0], ((X.shape[1] * X.shape[2]) * X.shape[3])))
        sigma = (np.dot(flatX.T, flatX) / flatX.shape[1])
        (U, S, V) = linalg.svd(sigma)
        self.principal_components = np.dot(np.dot(U, np.diag((1.0 / np.sqrt((S + 1e-06))))), U.T)