def tanh(x, name=None):
    'Computes hyperbolic tangent of `x` element-wise.\n\n  Args:\n    x: A Tensor or SparseTensor with type `float16`, `float32`, `double`,\n      `complex64`, or `complex128`.\n    name: A name for the operation (optional).\n\n  Returns:\n    A Tensor or SparseTensor respectively with the same type as `x`.\n  '
    with ops.name_scope(name, 'Tanh', [x]) as name:
        if isinstance(x, sparse_tensor.SparseTensor):
            x_tanh = gen_math_ops._tanh(x.values, name=name)
            return sparse_tensor.SparseTensor(indices=x.indices, values=x_tanh, dense_shape=x.dense_shape)
        else:
            return gen_math_ops._tanh(x, name=name)