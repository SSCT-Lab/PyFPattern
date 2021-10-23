def zeros(shape, dtype=dtypes.float32, name=None):
    'Creates a tensor with all elements set to zero.\n\n  This operation returns a tensor of type `dtype` with shape `shape` and\n  all elements set to zero.\n\n  For example:\n\n  ```python\n  tf.zeros([3, 4], int32) ==> [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]\n  ```\n\n  Args:\n    shape: Either a list of integers, or a 1-D `Tensor` of type `int32`.\n    dtype: The type of an element in the resulting `Tensor`.\n    name: A name for the operation (optional).\n\n  Returns:\n    A `Tensor` with all elements set to zero.\n  '
    dtype = dtypes.as_dtype(dtype).base_dtype
    with ops.name_scope(name, 'zeros', [shape]) as name:
        zero = (False if (dtype == dtypes.bool) else 0)
        try:
            shape = tensor_shape.as_shape(shape)
            output = constant(zero, shape=shape, dtype=dtype, name=name)
        except (TypeError, ValueError):
            shape = ops.convert_to_tensor(shape, dtype=dtypes.int32, name='shape')
            output = fill(shape, constant(zero, dtype=dtype), name=name)
    assert (output.dtype.base_dtype == dtype)
    return output