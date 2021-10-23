@tf_export('scatter_nd_add')
def scatter_nd_add(ref, indices, updates, use_locking=False, name=None):
    'Applies sparse addition to individual values or slices in a Variable.\n\n  `ref` is a `Tensor` with rank `P` and `indices` is a `Tensor` of rank `Q`.\n\n  `indices` must be integer tensor, containing indices into `ref`.\n  It must be shape `[d_0, ..., d_{Q-2}, K]` where `0 < K <= P`.\n\n  The innermost dimension of `indices` (with length `K`) corresponds to\n  indices into elements (if `K = P`) or slices (if `K < P`) along the `K`th\n  dimension of `ref`.\n\n  `updates` is `Tensor` of rank `Q-1+P-K` with shape:\n\n  ```\n  [d_0, ..., d_{Q-2}, ref.shape[K], ..., ref.shape[P-1]].\n  ```\n\n  For example, say we want to add 4 scattered elements to a rank-1 tensor to\n  8 elements. In Python, that update would look like this:\n\n  ```python\n      ref = tf.Variable([1, 2, 3, 4, 5, 6, 7, 8])\n      indices = tf.constant([[4], [3], [1] ,[7]])\n      updates = tf.constant([9, 10, 11, 12])\n      add = tf.scatter_nd_add(ref, indices, updates)\n      with tf.Session() as sess:\n        print sess.run(add)\n  ```\n\n  The resulting update to ref would look like this:\n\n      [1, 13, 3, 14, 14, 6, 7, 20]\n\n  See @{tf.scatter_nd} for more details about how to make updates to\n  slices.\n\n  Args:\n    ref: A mutable `Tensor`. Must be one of the following types: `float32`,\n      `float64`, `int32`, `uint8`, `int16`, `int8`, `complex64`, `int64`,\n      `qint8`, `quint8`, `qint32`, `bfloat16`, `uint16`, `complex128`, `half`,\n      `uint32`, `uint64`. A mutable Tensor. Should be from a Variable node.\n    indices: A `Tensor`. Must be one of the following types: `int32`, `int64`.\n      A tensor of indices into ref.\n    updates: A `Tensor`. Must have the same type as `ref`.\n      A tensor of updated values to add to ref.\n    use_locking: An optional `bool`. Defaults to `False`.\n      An optional bool. Defaults to True. If True, the assignment will\n      be protected by a lock; otherwise the behavior is undefined,\n      but may exhibit less contention.\n    name: A name for the operation (optional).\n\n  Returns:\n    A mutable `Tensor`. Has the same type as `ref`.\n  '
    if ref.dtype._is_ref_dtype:
        return gen_state_ops.scatter_nd_add(ref, indices, updates, use_locking, name)
    return ref._lazy_read(gen_state_ops.resource_scatter_nd_add(ref.handle, indices, ops.convert_to_tensor(updates, ref.dtype), name=name))