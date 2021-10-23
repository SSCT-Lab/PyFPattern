def cross(self, b):
    'Return the cross product of `self` and `b` relaxing the condition\n        of compatible dimensions: if each has 3 elements, a matrix of the\n        same type and shape as `self` will be returned. If `b` has the same\n        shape as `self` then common identities for the cross product (like\n        `a x b = - b x a`) will hold.\n\n        See Also\n        ========\n\n        dot\n        multiply\n        multiply_elementwise\n        '
    if (not is_sequence(b)):
        raise TypeError(('`b` must be an ordered iterable or Matrix, not %s.' % type(b)))
    if (not ((self.rows * self.cols) == (b.rows * b.cols) == 3)):
        raise ShapeError(('Dimensions incorrect for cross product: %s x %s' % ((self.rows, self.cols), (b.rows, b.cols))))
    else:
        return self._new(self.rows, self.cols, (((self[1] * b[2]) - (self[2] * b[1])), ((self[2] * b[0]) - (self[0] * b[2])), ((self[0] * b[1]) - (self[1] * b[0]))))