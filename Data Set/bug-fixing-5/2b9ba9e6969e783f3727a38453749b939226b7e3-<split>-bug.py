@tf_export('split')
def split(value, num_or_size_splits, axis=0, num=None, name='split'):
    "Splits a tensor into sub tensors.\n\n  If `num_or_size_splits` is an integer type, then splits `value`\n  along dimension `axis` into `num_split` smaller tensors.\n  Requires that `num_split` evenly divides `value.shape[axis]`.\n\n  If `num_or_size_splits` is not an integer type, it is presumed to be a Tensor\n  `size_splits`, then splits `value` into `len(size_splits)` pieces. The shape\n  of the `i`-th piece has the same size as the `value` except along dimension\n  `axis` where the size is `size_splits[i]`.\n\n  For example:\n\n  ```python\n  # 'value' is a tensor with shape [5, 30]\n  # Split 'value' into 3 tensors with sizes [4, 15, 11] along dimension 1\n  split0, split1, split2 = tf.split(value, [4, 15, 11], 1)\n  tf.shape(split0)  # [5, 4]\n  tf.shape(split1)  # [5, 15]\n  tf.shape(split2)  # [5, 11]\n  # Split 'value' into 3 tensors along dimension 1\n  split0, split1, split2 = tf.split(value, num_or_size_splits=3, axis=1)\n  tf.shape(split0)  # [5, 10]\n  ```\n\n  Args:\n    value: The `Tensor` to split.\n    num_or_size_splits: Either a 0-D integer `Tensor` indicating the number of\n      splits along split_dim or a 1-D integer `Tensor` containing\n      the sizes of each output tensor along split_dim. If a scalar then it must\n      evenly divide `value.shape[axis]`; otherwise the sum of sizes along the\n      split dimension must match that of the `value`.\n    axis: A 0-D `int32` `Tensor`. The dimension along which to split.\n      Must be in the range `[-rank(value), rank(value))`. Defaults to 0.\n    num: Optional, used to specify the number of outputs when it cannot be\n      inferred from the shape of `size_splits`.\n    name: A name for the operation (optional).\n\n  Returns:\n    if `num_or_size_splits` is a scalar returns `num_or_size_splits` `Tensor`\n    objects; if `num_or_size_splits` is a 1-D Tensor returns\n    `num_or_size_splits.get_shape[0]` `Tensor` objects resulting from splitting\n    `value`.\n\n  Raises:\n    ValueError: If `num` is unspecified and cannot be inferred.\n  "
    size_splits = ops.convert_to_tensor(num_or_size_splits)
    if ((size_splits._rank() == 0) and size_splits.dtype.is_integer):
        return gen_array_ops.split(axis=axis, num_split=num_or_size_splits, value=value, name=name)
    if (num is None):
        size_splits_shape = size_splits._shape_tuple()
        if size_splits_shape:
            num = size_splits_shape[0]
        if (num is None):
            raise ValueError(('Cannot infer num from shape %s' % num_or_size_splits))
    return gen_array_ops.split_v(value=value, size_splits=size_splits, axis=axis, num_split=num, name=name)