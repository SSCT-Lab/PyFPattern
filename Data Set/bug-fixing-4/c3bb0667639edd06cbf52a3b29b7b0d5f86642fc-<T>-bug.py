@property
def T(self):
    'Returns a copy of the array with axes transposed.\n\n        Equivalent to ``mx.nd.transpose(self)``.\n\n        Unlike ``numpy.ndarray.T``, this function only supports 2-D arrays,\n        and returns a copy rather than a view of the array.\n\n        Examples\n        --------\n        >>> x = mx.nd.arange(0,6).reshape((2,3))\n        >>> x.asnumpy()\n        array([[ 0.,  1.,  2.],\n               [ 3.,  4.,  5.]], dtype=float32)\n        >>> x.T.asnumpy()\n        array([[ 0.,  3.],\n               [ 1.,  4.],\n               [ 2.,  5.]], dtype=float32)\n\n        '
    if (len(self.shape) != 2):
        raise ValueError('Only 2D matrix is allowed to be transposed')
    return transpose(self)