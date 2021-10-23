def evaluate(self, points):
    'Evaluate the estimated pdf on a set of points.\n\n        Parameters\n        ----------\n        points : (# of dimensions, # of points)-array\n            Alternatively, a (# of dimensions,) vector can be passed in and\n            treated as a single point.\n\n        Returns\n        -------\n        values : (# of points,)-array\n            The values at each point.\n\n        Raises\n        ------\n        ValueError : if the dimensionality of the input points is different than\n                     the dimensionality of the KDE.\n\n        '
    points = atleast_2d(points)
    (d, m) = points.shape
    if (d != self.d):
        if ((d == 1) and (m == self.d)):
            points = reshape(points, (self.d, 1))
            m = 1
        else:
            msg = ('points have dimension %s, dataset has dimension %s' % (d, self.d))
            raise ValueError(msg)
    result = zeros((m,), dtype=float)
    whitening = linalg.cholesky(self.inv_cov)
    scaled_dataset = dot(whitening, self.dataset)
    scaled_points = dot(whitening, points)
    if (m >= self.n):
        for i in range(self.n):
            diff = (scaled_dataset[:, i, newaxis] - scaled_points)
            energy = (sum((diff * diff), axis=0) / 2.0)
            result += (self.weights[i] * exp((- energy)))
    else:
        for i in range(m):
            diff = (scaled_dataset - scaled_points[:, i, newaxis])
            energy = (sum((diff * diff), axis=0) / 2.0)
            result[i] = sum((exp((- energy)) * self.weights), axis=0)
    result = (result / self._norm_factor)
    return result