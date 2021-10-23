def lookup(self, row_labels, col_labels):
    '\n        Label-based "fancy indexing" function for DataFrame.\n\n        Given equal-length arrays of row and column labels, return an\n        array of the values corresponding to each (row, col) pair.\n\n        Parameters\n        ----------\n        row_labels : sequence\n            The row labels to use for lookup.\n        col_labels : sequence\n            The column labels to use for lookup.\n\n        Returns\n        -------\n        numpy.ndarray\n\n        Notes\n        -----\n        Akin to::\n\n            result = [df.get_value(row, col)\n                      for row, col in zip(row_labels, col_labels)]\n\n        Examples\n        --------\n        values : ndarray\n            The found values\n        '
    n = len(row_labels)
    if (n != len(col_labels)):
        raise ValueError('Row labels must have same size as column labels')
    thresh = 1000
    if ((not self._is_mixed_type) or (n > thresh)):
        values = self.values
        ridx = self.index.get_indexer(row_labels)
        cidx = self.columns.get_indexer(col_labels)
        if (ridx == (- 1)).any():
            raise KeyError('One or more row labels was not found')
        if (cidx == (- 1)).any():
            raise KeyError('One or more column labels was not found')
        flat_index = ((ridx * len(self.columns)) + cidx)
        result = values.flat[flat_index]
    else:
        result = np.empty(n, dtype='O')
        for (i, (r, c)) in enumerate(zip(row_labels, col_labels)):
            result[i] = self._get_value(r, c)
    if is_object_dtype(result):
        result = lib.maybe_convert_objects(result)
    return result