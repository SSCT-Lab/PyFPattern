def __init__(self, dataset, bw_method=None, weights=None):
    self.dataset = atleast_2d(asarray(dataset))
    if (not (self.dataset.size > 1)):
        raise ValueError('`dataset` input should have multiple elements.')
    (self.d, self.n) = self.dataset.shape
    if (weights is not None):
        self._weights = atleast_1d(weights).astype(float)
        self._weights /= sum(self._weights)
        if (self.weights.ndim != 1):
            raise ValueError('`weights` input should be one-dimensional.')
        if (len(self._weights) != self.n):
            raise ValueError('`weights` input should be of length n')
        self._neff = (1 / sum((self._weights ** 2)))
    self.set_bandwidth(bw_method=bw_method)