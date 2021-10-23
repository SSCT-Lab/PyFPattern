def dot(self, b):
    'Return the dot product of Matrix self and b relaxing the condition\n        of compatible dimensions: if either the number of rows or columns are\n        the same as the length of b then the dot product is returned. If self\n        is a row or column vector, a scalar is returned. Otherwise, a list\n        of results is returned (and in that case the number of columns in self\n        must match the length of b).\n\n        Examples\n        ========\n\n        >>> from sympy import Matrix\n        >>> M = Matrix([[1, 2, 3], [4, 5, 6], [7, 8, 9]])\n        >>> v = [1, 1, 1]\n        >>> M.row(0).dot(v)\n        6\n        >>> M.col(0).dot(v)\n        12\n        >>> M.dot(v)\n        [6, 15, 24]\n\n        See Also\n        ========\n\n        cross\n        multiply\n        multiply_elementwise\n        '
    from .dense import Matrix
    if (not isinstance(b, MatrixBase)):
        if is_sequence(b):
            if ((len(b) != self.cols) and (len(b) != self.rows)):
                raise ShapeError('Dimensions incorrect for dot product.')
            return self.dot(Matrix(b))
        else:
            raise TypeError(('`b` must be an ordered iterable or Matrix, not %s.' % type(b)))
    mat = self
    if (mat.cols == b.rows):
        if (b.cols != 1):
            mat = mat.T
            b = b.T
        prod = flatten((mat * b).tolist())
        if (len(prod) == 1):
            return prod[0]
        return prod
    if (mat.cols == b.cols):
        return mat.dot(b.T)
    elif (mat.rows == b.rows):
        return mat.T.dot(b)
    else:
        raise ShapeError('Dimensions incorrect for dot product.')