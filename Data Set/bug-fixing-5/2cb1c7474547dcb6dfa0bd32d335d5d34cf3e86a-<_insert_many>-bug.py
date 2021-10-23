def _insert_many(self, i, j, x):
    'Inserts new nonzero at each (i, j) with value x\n\n        Here (i,j) index major and minor respectively.\n        i, j and x must be non-empty, 1d arrays.\n        Inserts each major group (e.g. all entries per row) at a time.\n        Maintains has_sorted_indices property.\n        Modifies i, j, x in place.\n        '
    order = np.argsort(i, kind='mergesort')
    i = i.take(order, mode='clip')
    j = j.take(order, mode='clip')
    x = x.take(order, mode='clip')
    do_sort = self.has_sorted_indices
    idx_dtype = get_index_dtype((self.indices, self.indptr), maxval=(self.indptr[(- 1)] + x.size))
    self.indptr = np.asarray(self.indptr, dtype=idx_dtype)
    self.indices = np.asarray(self.indices, dtype=idx_dtype)
    i = np.asarray(i, dtype=idx_dtype)
    j = np.asarray(j, dtype=idx_dtype)
    indices_parts = []
    data_parts = []
    (ui, ui_indptr) = np.unique(i, return_index=True)
    ui_indptr = np.append(ui_indptr, len(j))
    new_nnzs = np.diff(ui_indptr)
    prev = 0
    for (c, (ii, js, je)) in enumerate(izip(ui, ui_indptr, ui_indptr[1:])):
        start = self.indptr[prev]
        stop = self.indptr[ii]
        indices_parts.append(self.indices[start:stop])
        data_parts.append(self.data[start:stop])
        (uj, uj_indptr) = np.unique(j[js:je][::(- 1)], return_index=True)
        if (len(uj) == (je - js)):
            indices_parts.append(j[js:je])
            data_parts.append(x[js:je])
        else:
            indices_parts.append(j[js:je][::(- 1)][uj_indptr])
            data_parts.append(x[js:je][::(- 1)][uj_indptr])
            new_nnzs[c] = len(uj)
        prev = ii
    start = self.indptr[ii]
    indices_parts.append(self.indices[start:])
    data_parts.append(self.data[start:])
    self.indices = np.concatenate(indices_parts)
    self.data = np.concatenate(data_parts)
    nnzs = np.asarray(np.ediff1d(self.indptr, to_begin=0), dtype=idx_dtype)
    nnzs[1:][ui] += new_nnzs
    self.indptr = np.cumsum(nnzs, out=nnzs)
    if do_sort:
        self.has_sorted_indices = False
        self.sort_indices()
    self.check_format(full_check=False)