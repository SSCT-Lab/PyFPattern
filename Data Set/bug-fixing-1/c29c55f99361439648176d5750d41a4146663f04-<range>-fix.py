

@tf_export('range')
def range(start, limit=None, delta=1, dtype=None, name='range'):
    'Creates a sequence of numbers.\n\n  Creates a sequence of numbers that begins at `start` and extends by\n  increments of `delta` up to but not including `limit`.\n\n  The dtype of the resulting tensor is inferred from the inputs unless\n  it is provided explicitly.\n\n  Like the Python builtin `range`, `start` defaults to 0, so that\n  `range(n) = range(0, n)`.\n\n  For example:\n\n  ```python\n  start = 3\n  limit = 18\n  delta = 3\n  tf.range(start, limit, delta)  # [3, 6, 9, 12, 15]\n\n  start = 3\n  limit = 1\n  delta = -0.5\n  tf.range(start, limit, delta)  # [3, 2.5, 2, 1.5]\n\n  limit = 5\n  tf.range(limit)  # [0, 1, 2, 3, 4]\n  ```\n\n  Args:\n    start: A 0-D `Tensor` (scalar). Acts as first entry in the range if `limit`\n      is not None; otherwise, acts as range limit and first entry defaults to 0.\n    limit: A 0-D `Tensor` (scalar). Upper limit of sequence, exclusive. If None,\n      defaults to the value of `start` while the first entry of the range\n      defaults to 0.\n    delta: A 0-D `Tensor` (scalar). Number that increments `start`. Defaults to\n      1.\n    dtype: The type of the elements of the resulting tensor.\n    name: A name for the operation. Defaults to "range".\n\n  Returns:\n    An 1-D `Tensor` of type `dtype`.\n\n  @compatibility(numpy)\n  Equivalent to np.arange\n  @end_compatibility\n  '
    if (limit is None):
        (start, limit) = (0, start)
    with ops.name_scope(name, 'Range', [start, limit, delta]) as name:
        if (dtype is not None):
            start = cast(start, dtype=dtype, name='start')
            limit = cast(limit, dtype=dtype, name='limit')
            delta = cast(delta, dtype=dtype, name='delta')
        else:
            start = ops.convert_to_tensor(start, name='start')
            limit = ops.convert_to_tensor(limit, name='limit')
            delta = ops.convert_to_tensor(delta, name='delta')
        if (dtype is None):
            dtype_hierarchy = [dtypes.int32, dtypes.int64, dtypes.float32, dtypes.float64]
            assert all(((arg.dtype in dtype_hierarchy) for arg in [start, limit, delta]))
            inferred_dtype = max([arg.dtype for arg in [start, limit, delta]], key=dtype_hierarchy.index)
            start = cast(start, inferred_dtype)
            limit = cast(limit, inferred_dtype)
            delta = cast(delta, inferred_dtype)
        return gen_math_ops._range(start, limit, delta, name=name)
