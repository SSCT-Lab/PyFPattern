def _maximum_minimum(self, other, npop, op_name, dense_check):
    if isscalarlike(other):
        if dense_check(other):
            warn('Taking maximum (minimum) with > 0 (< 0) number results to a dense matrix.', SparseEfficiencyWarning)
            other_arr = np.empty(self.shape, dtype=np.asarray(other).dtype)
            other_arr.fill(other)
            other_arr = self.__class__(other_arr)
            return self._binopt(other_arr, op_name)
        else:
            self.sum_duplicates()
            new_data = npop(self.data, np.asarray(other))
            mat = self.__class__((new_data, self.indices, self.indptr), dtype=new_data.dtype, shape=self.shape)
            return mat
    elif isdense(other):
        return npop(self.todense(), other)
    elif isspmatrix(other):
        return self._binopt(other, op_name)
    else:
        raise ValueError('Operands not compatible.')