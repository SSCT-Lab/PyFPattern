

def fit(self, x, augment=False, rounds=1, seed=None):
    'Fits internal statistics to some sample data.\n\n        Required for featurewise_center, featurewise_std_normalization\n        and zca_whitening.\n\n        # Arguments\n            x: Numpy array, the data to fit on. Should have rank 4.\n                In case of grayscale data,\n                the channels axis should have value 1, and in case\n                of RGB data, it should have value 3.\n            augment: Whether to fit on randomly augmented samples\n            rounds: If `augment`,\n                how many augmentation passes to do over the data\n            seed: random seed.\n\n        # Raises\n            ValueError: in case of invalid input `x`.\n        '
    x = np.asarray(x, dtype=K.floatx())
    if (x.ndim != 4):
        raise ValueError(('Input to `.fit()` should have rank 4. Got array with shape: ' + str(x.shape)))
    if (x.shape[self.channel_axis] not in {3, 4}):
        warnings.warn((((((((((('Expected input to be images (as Numpy array) following the data format convention "' + self.data_format) + '" (channels on axis ') + str(self.channel_axis)) + '), i.e. expected either 1, 3 or 4 channels on axis ') + str(self.channel_axis)) + '. However, it was passed an array with shape ') + str(x.shape)) + ' (') + str(x.shape[self.channel_axis])) + ' channels).'))
    if (seed is not None):
        np.random.seed(seed)
    x = np.copy(x)
    if augment:
        ax = np.zeros(tuple(([(rounds * x.shape[0])] + list(x.shape)[1:])), dtype=K.floatx())
        for r in range(rounds):
            for i in range(x.shape[0]):
                ax[(i + (r * x.shape[0]))] = self.random_transform(x[i])
        x = ax
    if self.featurewise_center:
        self.mean = np.mean(x, axis=(0, self.row_axis, self.col_axis))
        broadcast_shape = [1, 1, 1]
        broadcast_shape[(self.channel_axis - 1)] = x.shape[self.channel_axis]
        self.mean = np.reshape(self.mean, broadcast_shape)
        x -= self.mean
    if self.featurewise_std_normalization:
        self.std = np.std(x, axis=(0, self.row_axis, self.col_axis))
        broadcast_shape = [1, 1, 1]
        broadcast_shape[(self.channel_axis - 1)] = x.shape[self.channel_axis]
        self.std = np.reshape(self.std, broadcast_shape)
        x /= (self.std + K.epsilon())
    if self.zca_whitening:
        flat_x = np.reshape(x, (x.shape[0], ((x.shape[1] * x.shape[2]) * x.shape[3])))
        sigma = (np.dot(flat_x.T, flat_x) / flat_x.shape[0])
        (u, s, _) = linalg.svd(sigma)
        self.principal_components = np.dot(np.dot(u, np.diag((1.0 / np.sqrt((s + self.zca_epsilon))))), u.T)
