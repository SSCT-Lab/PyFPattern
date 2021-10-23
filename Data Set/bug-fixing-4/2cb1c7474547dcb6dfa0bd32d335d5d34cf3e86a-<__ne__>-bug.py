def __ne__(self, other):
    if isscalarlike(other):
        if np.isnan(other):
            warn('Comparing a sparse matrix with nan using != is inefficient', SparseEfficiencyWarning)
            all_true = self.__class__(np.ones(self.shape, dtype=np.bool_))
            return all_true
        elif (other != 0):
            warn('Comparing a sparse matrix with a nonzero scalar using != is inefficient, try using == instead.', SparseEfficiencyWarning)
            all_true = self.__class__(np.ones(self.shape), dtype=np.bool_)
            inv = self._scalar_binopt(other, operator.eq)
            return (all_true - inv)
        else:
            return self._scalar_binopt(other, operator.ne)
    elif isdense(other):
        return (self.todense() != other)
    elif isspmatrix(other):
        if (self.shape != other.shape):
            return True
        elif (self.format != other.format):
            other = other.asformat(self.format)
        return self._binopt(other, '_ne_')
    else:
        return True