

def matmul(a, b, transpose_a=False, transpose_b=False, adjoint_a=False, adjoint_b=False, a_is_sparse=False, b_is_sparse=False, name=None):
    'Multiplies matrix `a` by matrix `b`, producing `a` * `b`.\n\n  The inputs must be matrices (or tensors of rank > 2, representing batches of\n  matrices), with matching inner dimensions, possibly after transposition.\n\n  Both matrices must be of the same type. The supported types are:\n  `float16`, `float32`, `float64`, `int32`, `complex64`, `complex128`.\n\n  Either matrix can be transposed or adjointed (conjugated and transposed) on\n  the fly by setting one of the corresponding flag to `True`. These are `False`\n  by default.\n\n  If one or both of the matrices contain a lot of zeros, a more efficient\n  multiplication algorithm can be used by setting the corresponding\n  `a_is_sparse` or `b_is_sparse` flag to `True`. These are `False` by default.\n  This optimization is only available for plain matrices (rank-2 tensors) with\n  datatypes `bfloat16` or `float32`.\n\n  For example:\n\n  ```python\n  # 2-D tensor `a`\n  a = tf.constant([1, 2, 3, 4, 5, 6], shape=[2, 3]) => [[1. 2. 3.]\n                                                        [4. 5. 6.]]\n  # 2-D tensor `b`\n  b = tf.constant([7, 8, 9, 10, 11, 12], shape=[3, 2]) => [[7. 8.]\n                                                           [9. 10.]\n                                                           [11. 12.]]\n  c = tf.matmul(a, b) => [[58 64]\n                          [139 154]]\n\n\n  # 3-D tensor `a`\n  a = tf.constant(np.arange(1,13), shape=[2, 2, 3]) => [[[ 1.  2.  3.]\n                                                         [ 4.  5.  6.]],\n                                                        [[ 7.  8.  9.]\n                                                         [10. 11. 12.]]]\n\n  # 3-D tensor `b`\n  b = tf.constant(np.arange(13,25), shape=[2, 3, 2]) => [[[13. 14.]\n                                                          [15. 16.]\n                                                          [17. 18.]],\n                                                         [[19. 20.]\n                                                          [21. 22.]\n                                                          [23. 24.]]]\n  c = tf.matmul(a, b) => [[[ 94 100]\n                           [229 244]],\n                          [[508 532]\n                           [697 730]]]\n  ```\n\n  Args:\n    a: `Tensor` of type `float16`, `float32`, `float64`, `int32`, `complex64`,\n      `complex128` and rank > 1.\n    b: `Tensor` with same type and rank as `a`.\n    transpose_a: If `True`, `a` is transposed before multiplication.\n    transpose_b: If `True`, `b` is transposed before multiplication.\n    adjoint_a: If `True`, `a` is conjugated and transposed before\n      multiplication.\n    adjoint_b: If `True`, `b` is conjugated and transposed before\n      multiplication.\n    a_is_sparse: If `True`, `a` is treated as a sparse matrix.\n    b_is_sparse: If `True`, `b` is treated as a sparse matrix.\n    name: Name for the operation (optional).\n\n  Returns:\n    A `Tensor` of the same type as `a` and `b` where each inner-most matrix is\n    the product of the corresponding matrices in `a` and `b, e.g. if all\n    transpose or adjoint attributes are `False`:\n\n    output[..., :, :] = a[..., :, :] * b[..., :, :] ,\n\n\n  Raises:\n    ValueError: If transpose_a and adjoint_a, or transpose_b and adjoint_b\n      are both set to True.\n  '
    with ops.name_scope(name, 'MatMul', [a, b]) as name:
        if (transpose_a and adjoint_a):
            raise ValueError('Only one of transpose_a and adjoint_a can be True.')
        if (transpose_b and adjoint_b):
            raise ValueError('Only one of transpose_b and adjoint_b can be True.')
        a = ops.convert_to_tensor(a, name='a')
        b = ops.convert_to_tensor(b, name='b')
        a_shape = a.get_shape()
        b_shape = b.get_shape()
        if (((not a_is_sparse) and (not b_is_sparse)) and (((a_shape.ndims is None) or (a_shape.ndims > 2)) and ((b_shape.ndims is None) or (b_shape.ndims > 2)))):
            if transpose_a:
                a = conj(a)
                adjoint_a = True
            if transpose_b:
                b = conj(b)
                adjoint_b = True
            return gen_math_ops._batch_mat_mul(a, b, adj_x=adjoint_a, adj_y=adjoint_b, name=name)
        if adjoint_a:
            a = conj(a)
            transpose_a = True
        if adjoint_b:
            b = conj(b)
            transpose_b = True
        sparse_matmul_types = [dtypes.bfloat16, dtypes.float32]
        use_sparse_matmul = ((a.dtype in sparse_matmul_types) and (b.dtype in sparse_matmul_types) and (a_is_sparse or b_is_sparse))
        if (dtypes.bfloat16 in (a.dtype, b.dtype)):
            use_sparse_matmul = True
        if use_sparse_matmul:
            return sparse_matmul(a, b, transpose_a=transpose_a, transpose_b=transpose_b, a_is_sparse=a_is_sparse, b_is_sparse=b_is_sparse, name=name)
        else:
            return gen_math_ops._mat_mul(a, b, transpose_a=transpose_a, transpose_b=transpose_b, name=name)
