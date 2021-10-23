def __init__(self, arg1, shape=None, dtype=None, copy=False):
    _data_matrix.__init__(self)
    if isinstance(arg1, tuple):
        if isshape(arg1):
            (M, N) = arg1
            self._shape = check_shape((M, N))
            idx_dtype = get_index_dtype(maxval=max(M, N))
            self.row = np.array([], dtype=idx_dtype)
            self.col = np.array([], dtype=idx_dtype)
            self.data = np.array([], getdtype(dtype, default=float))
            self.has_canonical_format = True
        else:
            try:
                (obj, (row, col)) = arg1
            except (TypeError, ValueError):
                raise TypeError('invalid input format')
            if (shape is None):
                if ((len(row) == 0) or (len(col) == 0)):
                    raise ValueError('cannot infer dimensions from zero sized index arrays')
                M = (operator.index(np.max(row)) + 1)
                N = (operator.index(np.max(col)) + 1)
                self._shape = check_shape((M, N))
            else:
                (M, N) = shape
                self._shape = check_shape((M, N))
            idx_dtype = get_index_dtype(maxval=max(self.shape))
            self.row = np.array(row, copy=copy, dtype=idx_dtype)
            self.col = np.array(col, copy=copy, dtype=idx_dtype)
            self.data = np.array(obj, copy=copy)
            self.has_canonical_format = False
    elif isspmatrix(arg1):
        if (isspmatrix_coo(arg1) and copy):
            self.row = arg1.row.copy()
            self.col = arg1.col.copy()
            self.data = arg1.data.copy()
            self._shape = check_shape(arg1.shape)
        else:
            coo = arg1.tocoo()
            self.row = coo.row
            self.col = coo.col
            self.data = coo.data
            self._shape = check_shape(coo.shape)
        self.has_canonical_format = False
    else:
        M = np.atleast_2d(np.asarray(arg1))
        if (M.ndim != 2):
            raise TypeError('expected dimension <= 2 array or matrix')
        else:
            self._shape = check_shape(M.shape)
        (self.row, self.col) = M.nonzero()
        self.data = M[(self.row, self.col)]
        self.has_canonical_format = True
    if (dtype is not None):
        self.data = self.data.astype(dtype, copy=False)
    self._check()