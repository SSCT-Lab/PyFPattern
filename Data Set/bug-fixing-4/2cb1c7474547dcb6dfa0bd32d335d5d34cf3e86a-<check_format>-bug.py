def check_format(self, full_check=True):
    'check whether the matrix format is valid\n\n        Parameters\n        ----------\n        full_check : bool, optional\n            If `True`, rigorous check, O(N) operations. Otherwise\n            basic check, O(1) operations (default True).\n        '
    (major_name, minor_name) = self._swap(('row', 'column'))
    (major_dim, minor_dim) = self._swap(self.shape)
    if (self.indptr.dtype.kind != 'i'):
        warn(('indptr array has non-integer dtype (%s)' % self.indptr.dtype.name))
    if (self.indices.dtype.kind != 'i'):
        warn(('indices array has non-integer dtype (%s)' % self.indices.dtype.name))
    idx_dtype = get_index_dtype((self.indptr, self.indices))
    self.indptr = np.asarray(self.indptr, dtype=idx_dtype)
    self.indices = np.asarray(self.indices, dtype=idx_dtype)
    self.data = to_native(self.data)
    if ((self.data.ndim != 1) or (self.indices.ndim != 1) or (self.indptr.ndim != 1)):
        raise ValueError('data, indices, and indptr should be 1-D')
    if (len(self.indptr) != (major_dim + 1)):
        raise ValueError(('index pointer size (%d) should be (%d)' % (len(self.indptr), (major_dim + 1))))
    if (self.indptr[0] != 0):
        raise ValueError('index pointer should start with 0')
    if (len(self.indices) != len(self.data)):
        raise ValueError('indices and data should have the same size')
    if (self.indptr[(- 1)] > len(self.indices)):
        raise ValueError('Last value of index pointer should be less than the size of index and data arrays')
    self.prune()
    if full_check:
        if (self.nnz > 0):
            if (self.indices.max() >= minor_dim):
                raise ValueError(('%s index values must be < %d' % (minor_name, minor_dim)))
            if (self.indices.min() < 0):
                raise ValueError(('%s index values must be >= 0' % minor_name))
            if (np.diff(self.indptr).min() < 0):
                raise ValueError('index pointer values must form a non-decreasing sequence')