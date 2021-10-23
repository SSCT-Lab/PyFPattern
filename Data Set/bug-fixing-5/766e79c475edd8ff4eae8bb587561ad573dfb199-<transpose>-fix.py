def transpose(a, perm=None, name='transpose'):
    "Transposes `a`. Permutes the dimensions according to `perm`.\n\n  The returned tensor's dimension i will correspond to the input dimension\n  `perm[i]`. If `perm` is not given, it is set to (n-1...0), where n is\n  the rank of the input tensor. Hence by default, this operation performs a\n  regular matrix transpose on 2-D input Tensors.\n\n  For example:\n\n  ```python\n  # 'x' is [[1 2 3]\n  #         [4 5 6]]\n  tf.transpose(x) ==> [[1 4]\n                       [2 5]\n                       [3 6]]\n\n  # Equivalently\n  tf.transpose(x, perm=[1, 0]) ==> [[1 4]\n                                    [2 5]\n                                    [3 6]]\n\n  # 'perm' is more useful for n-dimensional tensors, for n > 2\n  # 'x' is   [[[1  2  3]\n  #            [4  5  6]]\n  #           [[7  8  9]\n  #            [10 11 12]]]\n  # Take the transpose of the matrices in dimension-0\n  tf.transpose(x, perm=[0, 2, 1]) ==> [[[1  4]\n                                        [2  5]\n                                        [3  6]]\n\n                                       [[7 10]\n                                        [8 11]\n                                        [9 12]]]\n  ```\n\n  Args:\n    a: A `Tensor`.\n    perm: A permutation of the dimensions of `a`.\n    name: A name for the operation (optional).\n\n  Returns:\n    A transposed `Tensor`.\n  "
    with ops.op_scope([a], name, 'transpose') as name:
        if (perm is None):
            rank = gen_array_ops.rank(a)
            perm = ((rank - 1) - gen_math_ops._range(0, rank, 1))
            ret = gen_array_ops.transpose(a, perm, name=name)
            input_shape = ret.op.inputs[0].get_shape().dims
            if (input_shape is not None):
                ret.set_shape(input_shape[::(- 1)])
        else:
            ret = gen_array_ops.transpose(a, perm, name=name)
        return ret