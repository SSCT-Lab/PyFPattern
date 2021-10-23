def ones(shape, dtype=dtypes.float32, name=None):
    'Creates a tensor with all elements set to 1.\n\n  This operation returns a tensor of type `dtype` with shape `shape` and all\n  elements set to 1.\n\n  For example:\n\n  ```python\n  tf.ones([2, 3], int32) ==> [[1, 1, 1], [1, 1, 1]]\n  ```\n\n  Args:\n    shape: Either a list of integers, or a 1-D `Tensor` of type `int32`.\n    dtype: The type of an element in the resulting `Tensor`.\n    name: A name for the operation (optional).\n\n  Returns:\n    A `Tensor` with all elements set to 1.\n  '
    dtype = dtypes.as_dtype(dtype).base_dtype
    with ops.name_scope(name, 'ones', [shape]) as name:
        one = (True if (dtype == dtypes.bool) else 1)
        try:
            shape = tensor_shape.as_shape(shape)
            output = constant(one, shape=shape, dtype=dtype, name=name)
        except (TypeError, ValueError):
            shape = ops.convert_to_tensor(shape, dtype=dtypes.int32, name='shape')
            output = fill(shape, constant(one, dtype=dtype), name=name)
    assert (output.dtype.base_dtype == dtype)
    return output