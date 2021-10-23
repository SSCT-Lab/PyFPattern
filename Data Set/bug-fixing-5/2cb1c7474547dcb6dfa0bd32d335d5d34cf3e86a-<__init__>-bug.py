def __init__(self, arg1, shape=None, dtype=None, copy=False):
    _data_matrix.__init__(self)
    if isspmatrix(arg1):
        if ((arg1.format == self.format) and copy):
            arg1 = arg1.copy()
        else:
            arg1 = arg1.asformat(self.format)
        self._set_self(arg1)
    elif isinstance(arg1, tuple):
        if isshape(arg1):
            self._shape = check_shape(arg1)
            (M, N) = self.shape
            idx_dtype = get_index_dtype(maxval=max(M, N))
            self.data = np.zeros(0, getdtype(dtype, default=float))
            self.indices = np.zeros(0, idx_dtype)
            self.indptr = np.zeros((self._swap((M, N))[0] + 1), dtype=idx_dtype)
        elif (len(arg1) == 2):
            from .coo import coo_matrix
            other = self.__class__(coo_matrix(arg1, shape=shape))
            self._set_self(other)
        elif (len(arg1) == 3):
            (data, indices, indptr) = arg1
            maxval = None
            if (shape is not None):
                maxval = max(shape)
            idx_dtype = get_index_dtype((indices, indptr), maxval=maxval, check_contents=True)
            self.indices = np.array(indices, copy=copy, dtype=idx_dtype)
            self.indptr = np.array(indptr, copy=copy, dtype=idx_dtype)
            self.data = np.array(data, copy=copy, dtype=dtype)
        else:
            raise ValueError(('unrecognized %s_matrix constructor usage' % self.format))
    else:
        try:
            arg1 = np.asarray(arg1)
        except Exception:
            raise ValueError(('unrecognized %s_matrix constructor usage' % self.format))
        from .coo import coo_matrix
        self._set_self(self.__class__(coo_matrix(arg1, dtype=dtype)))
    if (shape is not None):
        self._shape = check_shape(shape)
    elif (self.shape is None):
        try:
            major_dim = (len(self.indptr) - 1)
            minor_dim = (self.indices.max() + 1)
        except Exception:
            raise ValueError('unable to infer matrix dimensions')
        else:
            self._shape = check_shape(self._swap((major_dim, minor_dim)))
    if (dtype is not None):
        self.data = np.asarray(self.data, dtype=dtype)
    self.check_format(full_check=False)