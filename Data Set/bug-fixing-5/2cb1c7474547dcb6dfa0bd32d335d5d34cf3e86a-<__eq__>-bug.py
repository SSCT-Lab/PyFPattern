def __eq__(self, other):
    if isscalarlike(other):
        if np.isnan(other):
            return self.__class__(self.shape, dtype=np.bool_)
        if (other == 0):
            warn('Comparing a sparse matrix with 0 using == is inefficient, try using != instead.', SparseEfficiencyWarning)
            all_true = self.__class__(np.ones(self.shape, dtype=np.bool_))
            inv = self._scalar_binopt(other, operator.ne)
            return (all_true - inv)
        else:
            return self._scalar_binopt(other, operator.eq)
    elif isdense(other):
        return (self.todense() == other)
    elif isspmatrix(other):
        warn('Comparing sparse matrices using == is inefficient, try using != instead.', SparseEfficiencyWarning)
        if (self.shape != other.shape):
            return False
        elif (self.format != other.format):
            other = other.asformat(self.format)
        res = self._binopt(other, '_ne_')
        all_true = self.__class__(np.ones(self.shape, dtype=np.bool_))
        return (all_true - res)
    else:
        return False