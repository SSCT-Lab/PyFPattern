

def astype(self, dtype, copy=True):
    "Return a copy of the array after casting to a specified type.\n\n        Parameters\n        ----------\n        dtype : numpy.dtype or str\n            The type of the returned array.\n        copy : bool\n            Default `True`. By default, astype always returns a newly\n            allocated ndarray on the same context. If this is set to\n            `False`, and the dtype requested is the same as the ndarray's\n            dtype, the ndarray is returned instead of a copy.\n\n        Examples\n        --------\n        >>> x = mx.nd.sparse.zeros('row_sparse', (2,3), dtype='float32')\n        >>> y = x.astype('int32')\n        >>> y.dtype\n        <type 'numpy.int32'>\n        "
    if ((not copy) and (np.dtype(dtype) == self.dtype)):
        return self
    res = zeros(shape=self.shape, ctx=self.context, dtype=dtype, stype=self.stype)
    self.copyto(res)
    return res
