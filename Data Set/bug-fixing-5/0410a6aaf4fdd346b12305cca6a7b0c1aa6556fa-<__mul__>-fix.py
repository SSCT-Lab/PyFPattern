def __mul__(self, other):
    'Return self*other where other is either a scalar or a matrix\n        of compatible dimensions.\n\n        Examples\n        ========\n\n        >>> from sympy.matrices import Matrix\n        >>> A = Matrix([[1, 2, 3], [4, 5, 6]])\n        >>> 2*A == A*2 == Matrix([[2, 4, 6], [8, 10, 12]])\n        True\n        >>> B = Matrix([[1, 2, 3], [4, 5, 6], [7, 8, 9]])\n        >>> A*B\n        Matrix([\n        [30, 36, 42],\n        [66, 81, 96]])\n        >>> B*A\n        Traceback (most recent call last):\n        ...\n        ShapeError: Matrices size mismatch.\n        >>>\n\n        See Also\n        ========\n\n        matrix_multiply_elementwise\n        '
    if getattr(other, 'is_Matrix', False):
        A = self
        B = other
        if (A.cols != B.rows):
            raise ShapeError(('Matrix size mismatch: %s * %s.' % (A.shape, B.shape)))
        if (A.cols == 0):
            return classof(A, B)._new(A.rows, B.cols, (lambda i, j: 0))
        try:
            blst = B.T.tolist()
        except AttributeError:
            return NotImplemented
        alst = A.tolist()
        return classof(A, B)._new(A.rows, B.cols, (lambda i, j: reduce((lambda k, l: (k + l)), [(a_ik * b_kj) for (a_ik, b_kj) in zip(alst[i], blst[j])])))
    else:
        return self._new(self.rows, self.cols, [(i * other) for i in self._mat])