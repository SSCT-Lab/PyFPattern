def _set_many(self, i, j, x):
    'Sets value at each (i, j) to x\n\n        Here (i,j) index major and minor respectively, and must not contain\n        duplicate entries.\n        '
    (i, j, M, N) = self._prepare_indices(i, j)
    n_samples = len(x)
    offsets = np.empty(n_samples, dtype=self.indices.dtype)
    ret = _sparsetools.csr_sample_offsets(M, N, self.indptr, self.indices, n_samples, i, j, offsets)
    if (ret == 1):
        self.sum_duplicates()
        _sparsetools.csr_sample_offsets(M, N, self.indptr, self.indices, n_samples, i, j, offsets)
    if ((- 1) not in offsets):
        self.data[offsets] = x
        return
    else:
        warn(('Changing the sparsity structure of a %s_matrix is expensive. lil_matrix is more efficient.' % self.format), SparseEfficiencyWarning)
        mask = (offsets > (- 1))
        self.data[offsets[mask]] = x[mask]
        mask = (~ mask)
        i = i[mask]
        i[(i < 0)] += M
        j = j[mask]
        j[(j < 0)] += N
        self._insert_many(i, j, x[mask])