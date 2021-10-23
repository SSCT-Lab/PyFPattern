def _get_submatrix(self, slice0, slice1):
    'Return a submatrix of this matrix (new matrix is created).'
    (slice0, slice1) = self._swap((slice0, slice1))
    (shape0, shape1) = self._swap(self.shape)

    def _process_slice(sl, num):
        if isinstance(sl, slice):
            (i0, i1) = (sl.start, sl.stop)
            if (i0 is None):
                i0 = 0
            elif (i0 < 0):
                i0 = (num + i0)
            if (i1 is None):
                i1 = num
            elif (i1 < 0):
                i1 = (num + i1)
            return (i0, i1)
        elif np.isscalar(sl):
            if (sl < 0):
                sl += num
            return (sl, (sl + 1))
        else:
            return (sl[0], sl[1])

    def _in_bounds(i0, i1, num):
        if ((not (0 <= i0 < num)) or (not (0 < i1 <= num)) or (not (i0 < i1))):
            raise IndexError('index out of bounds: 0<={i0}<{num}, 0<={i1}<{num}, {i0}<{i1}'.format(i0=i0, num=num, i1=i1))
    (i0, i1) = _process_slice(slice0, shape0)
    (j0, j1) = _process_slice(slice1, shape1)
    _in_bounds(i0, i1, shape0)
    _in_bounds(j0, j1, shape1)
    aux = _sparsetools.get_csr_submatrix(shape0, shape1, self.indptr, self.indices, self.data, i0, i1, j0, j1)
    (data, indices, indptr) = (aux[2], aux[1], aux[0])
    shape = self._swap(((i1 - i0), (j1 - j0)))
    return self.__class__((data, indices, indptr), shape=shape)