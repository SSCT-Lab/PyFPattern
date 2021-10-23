

def abs(x, name=None):
    "Computes the absolute value of a tensor.\n\n  Given a tensor of real numbers `x`, this operation returns a tensor\n  containing the absolute value of each element in `x`. For example, if x is\n  an input element and y is an output element, this operation computes\n  \\(y = |x|\\).\n\n  Given a tensor `x` of complex numbers, this operation returns a tensor of type\n  `float32` or `float64` that is the absolute value of each element in `x`. All\n  elements in `x` must be complex numbers of the form \\(a + bj\\). The\n  absolute value is computed as \\( \\sqrt{a^2 + b^2}\\).  For example:\n  ```\n  # tensor 'x' is [[-2.25 + 4.75j], [-3.25 + 5.75j]]\n  tf.complex_abs(x) ==> [5.25594902, 6.60492229]\n  ```\n\n  Args:\n    x: A `Tensor` or `SparseTensor` of type `float32`, `float64`, `int32`,\n      `int64`, `complex64` or `complex128`.\n    name: A name for the operation (optional).\n\n  Returns:\n    A `Tensor` or `SparseTensor` the same size and type as `x` with absolute\n      values.\n    Note, for `complex64` or `complex128' input, the returned `Tensor` will be\n      of type `float32` or `float64`, respectively.\n  "
    with ops.name_scope(name, 'Abs', [x]) as name:
        if isinstance(x, sparse_tensor.SparseTensor):
            if (x.values.dtype in (dtypes.complex64, dtypes.complex128)):
                x_abs = gen_math_ops._complex_abs(x.values, Tout=x.values.dtype.real_dtype, name=name)
                return sparse_tensor.SparseTensor(indices=x.indices, values=x_abs, dense_shape=x.dense_shape)
            x_abs = gen_math_ops._abs(x.values, name=name)
            return sparse_tensor.SparseTensor(indices=x.indices, values=x_abs, dense_shape=x.dense_shape)
        else:
            x = ops.convert_to_tensor(x, name='x')
            if (x.dtype in (dtypes.complex64, dtypes.complex128)):
                return gen_math_ops._complex_abs(x, Tout=x.dtype.real_dtype, name=name)
            return gen_math_ops._abs(x, name=name)
