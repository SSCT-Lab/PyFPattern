

def as_real_imag(self):
    "Returns a tuple of the real part of the input Matrix\n           and it's imaginary part.\n\n           >>> from sympy import Matrix, I\n           >>> A = Matrix([[1+2*I,3],[4+7*I,5]])\n           >>> A.as_real_imag()\n           (Matrix([\n           [1, 3],\n           [4, 5]]), Matrix([\n           [2, 0],\n           [7, 0]]))\n           >>> from sympy.abc import x, y, z, w\n           >>> B = Matrix([[x, y + x * I],[z + w * I, z]])\n           >>> B.as_real_imag()\n           (Matrix([\n           [        re(x), re(y) - im(x)],\n           [re(z) - im(w),         re(z)]]), Matrix([\n           [        im(x), re(x) + im(y)],\n           [re(w) + im(z),         im(z)]]))\n\n        "
    from sympy.functions.elementary.complexes import re, im
    real_mat = self._new(self.rows, self.cols, (lambda i, j: re(self[(i, j)])))
    im_mat = self._new(self.rows, self.cols, (lambda i, j: im(self[(i, j)])))
    return (real_mat, im_mat)
