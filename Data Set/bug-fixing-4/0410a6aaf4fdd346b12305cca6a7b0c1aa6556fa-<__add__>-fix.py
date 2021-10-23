def __add__(self, other):
    "Return self + other, raising ShapeError if shapes don't match."
    if getattr(other, 'is_Matrix', False):
        A = self
        B = other
        if (A.shape != B.shape):
            raise ShapeError(('Matrix size mismatch: %s + %s' % (A.shape, B.shape)))
        alst = A.tolist()
        blst = B.tolist()
        ret = ([S.Zero] * A.rows)
        for i in range(A.shape[0]):
            ret[i] = [(j + k) for (j, k) in zip(alst[i], blst[i])]
        rv = classof(A, B)._new(ret)
        if (0 in A.shape):
            rv = rv.reshape(*A.shape)
        return rv
    raise TypeError(('cannot add matrix and %s' % type(other)))