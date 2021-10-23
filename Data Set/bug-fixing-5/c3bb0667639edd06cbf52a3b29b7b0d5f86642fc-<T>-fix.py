@property
def T(self):
    'Returns a copy of the array with axes transposed.\n\n        Equivalent to ``mx.nd.transpose(self)`` except that\n        self is returned if ``self.ndim < 2``.\n\n        Unlike ``numpy.ndarray.T``, this function returns a copy\n        rather than a view of the array unless ``self.ndim < 2``.\n\n        Examples\n        --------\n        >>> x = mx.nd.arange(0,6).reshape((2,3))\n        >>> x.asnumpy()\n        array([[ 0.,  1.,  2.],\n               [ 3.,  4.,  5.]], dtype=float32)\n        >>> x.T.asnumpy()\n        array([[ 0.,  3.],\n               [ 1.,  4.],\n               [ 2.,  5.]], dtype=float32)\n\n        '
    if (len(self.shape) < 2):
        return self
    return transpose(self)