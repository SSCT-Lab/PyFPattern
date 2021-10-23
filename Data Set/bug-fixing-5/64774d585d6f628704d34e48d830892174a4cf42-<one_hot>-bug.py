def one_hot(indices, depth, on_value=1, off_value=0, axis=None, dtype=dtypes.float32, name=None):
    'Returns a one-hot tensor.\n\n  The locations represented by indices in `indices` take value `on_value`,\n  while all other locations take value `off_value`. By default, `on_value` is 1,\n  and `off_value` is 0. The type of the output tensor is specified by `dtype`, \n  which defaults to `tf.float32`.\n\n  If the input `indices` is rank `N`, the output will have rank `N+1`. The\n  new axis is created at dimension `axis` (default: the new axis is appended\n  at the end).\n\n  If `indices` is a scalar the output shape will be a vector of length `depth`\n\n  If `indices` is a vector of length `features`, the output shape will be:\n  ```\n    features x depth if axis == -1\n    depth x features if axis == 0\n  ```\n\n  If `indices` is a matrix (batch) with shape `[batch, features]`, the output\n  shape will be:\n  ```\n    batch x features x depth if axis == -1\n    batch x depth x features if axis == 1\n    depth x batch x features if axis == 0\n  ```\n\n\n  Examples\n  =========\n\n  Suppose that\n\n  ```\n    indices = [0, 2, -1, 1]\n    depth = 3\n    on_value = 5.0\n    off_value = 0.0\n    axis = -1\n  ```\n\n  Then output is `[4 x 3]`:\n\n  ```output =\n    [5.0 0.0 0.0]  // one_hot(0)\n    [0.0 0.0 5.0]  // one_hot(2)\n    [0.0 0.0 0.0]  // one_hot(-1)\n    [0.0 5.0 0.0]  // one_hot(1)\n  ```\n\n  Suppose that\n\n  ```\n    indices = [[0, 2], [1, -1]]\n    depth = 3\n    on_value = 1.0\n    off_value = 0.0\n    axis = -1\n  ```\n\n  Then output is `[2 x 2 x 3]`:\n\n  ```\n    output =\n    [\n      [1.0, 0.0, 0.0]  // one_hot(0)\n      [0.0, 0.0, 1.0]  // one_hot(2)\n    ][\n      [0.0, 1.0, 0.0]  // one_hot(1)\n      [0.0, 0.0, 0.0]  // one_hot(-1)\n    ]\n  ```\n\n  Args:\n    indices: A `Tensor` of indices.\n    depth: A scalar defining the depth of the one hot dimension.\n    on_value: A scalar defining the value to fill in output when `indices[j]\n      = i`. (default: 1)\n    off_value: A scalar defining the value to fill in output when `indices[j]\n      != i`. (default: 0)\n    axis: The axis to fill (default: -1, a new inner-most axis).\n    dtype: The data type of the output tensor.\n\n  Returns:\n    output: The one-hot tensor.\n\n  Raises:\n    TypeError: If dtype is `tf.string`\n  '
    if (dtype == dtypes.string):
        raise TypeError('dtype must be a numeric type')
    with ops.op_scope([indices, depth, on_value, off_value, axis, dtype], name, 'one_hot') as name:
        on_value = ops.convert_to_tensor(on_value, dtype=dtype, name='on_value')
        off_value = ops.convert_to_tensor(off_value, dtype=dtype, name='off_value')
        indices = ops.convert_to_tensor(indices, dtype=dtypes.int64, name='indices')
        depth = ops.convert_to_tensor(depth, dtype=dtypes.int32, name='depth')
        return gen_array_ops._one_hot(indices, depth, on_value, off_value, axis, name)