

def size(input, name=None, out_type=dtypes.int32):
    'Returns the size of a tensor.\n\n  This operation returns an integer representing the number of elements in\n  `input`.\n\n  For example:\n\n  ```python\n  t = tf.constant([[[1, 1, 1], [2, 2, 2]], [[3, 3, 3], [4, 4, 4]]])\n  tf.size(t)  # 12\n  ```\n\n  Args:\n    input: A `Tensor` or `SparseTensor`.\n    name: A name for the operation (optional).\n    out_type: (Optional) The specified output type of the operation\n      (`int32` or `int64`). Defaults to tf.int32.\n\n  Returns:\n    A `Tensor` of type `out_type`. Defaults to tf.int32.\n  '
    return size_internal(input, name, optimize=True, out_type=out_type)
