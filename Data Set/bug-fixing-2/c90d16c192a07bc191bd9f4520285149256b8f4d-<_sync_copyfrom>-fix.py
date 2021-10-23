

def _sync_copyfrom(self, source_array):
    'Performs a synchronized copy from the `source_array` to the current array.\n        This is called through ``x[:] = source_array``, where the `source_array`\n        is a `numpy.ndarray` or array-like object.\n        This function blocks until all the pending read/write operations with respect\n        to the current `NDArray` are finished and carry out the copy operation to the\n        current NDArray.\n\n        Parameters\n        ----------\n        source_array : array_like\n            The data source we would like to copy from.\n\n        Example\n        -------\n        >>> a = mx.nd.array([1, 2])\n        >>> a.asnumpy()\n        array([ 1.,  2.], dtype=float32)\n        >>> a[:] = np.array([3, 4])\n        >> a.asnumpy()\n        array([ 3.,  4.], dtype=float32)\n        '
    if (not isinstance(source_array, np.ndarray)):
        try:
            source_array = np.array(source_array, dtype=self.dtype)
        except:
            raise TypeError(('array must consist of array-like data,' + ('type %s is not supported' % str(type(array)))))
    source_array = np.asarray(source_array, dtype=self.dtype, order='C')
    if (source_array.shape != self.shape):
        raise ValueError(('Shape inconsistent: expected %s vs got %s' % (str(source_array.shape), str(self.shape))))
    check_call(_LIB.MXNDArraySyncCopyFromCPU(self.handle, source_array.ctypes.data_as(ctypes.c_void_p), ctypes.c_size_t(source_array.size)))
