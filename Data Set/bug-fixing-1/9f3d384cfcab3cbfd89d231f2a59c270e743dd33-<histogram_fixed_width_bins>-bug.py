

@tf_export('histogram_fixed_width_bins')
def histogram_fixed_width_bins(values, value_range, nbins=100, dtype=dtypes.int32, name=None):
    "Bins the given values for use in a histogram.\n\n  Given the tensor `values`, this operation returns a rank 1 `Tensor`\n  representing the indices of a histogram into which each element\n  of `values` would be binned. The bins are equal width and\n  determined by the arguments `value_range` and `nbins`.\n\n  Args:\n    values:  Numeric `Tensor`.\n    value_range:  Shape [2] `Tensor` of same `dtype` as `values`.\n      values <= value_range[0] will be mapped to hist[0],\n      values >= value_range[1] will be mapped to hist[-1].\n    nbins:  Scalar `int32 Tensor`.  Number of histogram bins.\n    dtype:  dtype for returned histogram.\n    name:  A name for this operation (defaults to 'histogram_fixed_width').\n\n  Returns:\n    A `Tensor` holding the indices of the binned values whose shape matches\n    `values`.\n\n  Examples:\n\n  ```python\n  # Bins will be:  (-inf, 1), [1, 2), [2, 3), [3, 4), [4, inf)\n  nbins = 5\n  value_range = [0.0, 5.0]\n  new_values = [-1.0, 0.0, 1.5, 2.0, 5.0, 15]\n\n  with tf.compat.v1.get_default_session() as sess:\n    indices = tf.histogram_fixed_width_bins(new_values, value_range, nbins=5)\n    variables.global_variables_initializer().run()\n    sess.run(indices) => [0, 0, 1, 2, 4]\n  ```\n  "
    with ops.name_scope(name, 'histogram_fixed_width_bins', [values, value_range, nbins]):
        values = ops.convert_to_tensor(values, name='values')
        shape = array_ops.shape(values)
        values = array_ops.reshape(values, [(- 1)])
        value_range = ops.convert_to_tensor(value_range, name='value_range')
        nbins = ops.convert_to_tensor(nbins, dtype=dtypes.int32, name='nbins')
        nbins_float = math_ops.cast(nbins, values.dtype)
        scaled_values = math_ops.truediv((values - value_range[0]), (value_range[1] - value_range[0]), name='scaled_values')
        indices = math_ops.floor((nbins_float * scaled_values), name='indices')
        indices = math_ops.cast(clip_ops.clip_by_value(indices, 0, (nbins_float - 1)), dtypes.int32)
        return array_ops.reshape(indices, shape)
