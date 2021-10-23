@tf_export('histogram_fixed_width')
def histogram_fixed_width(values, value_range, nbins=100, dtype=dtypes.int32, name=None):
    "Return histogram of values.\n\n  Given the tensor `values`, this operation returns a rank 1 histogram counting\n  the number of entries in `values` that fell into every bin.  The bins are\n  equal width and determined by the arguments `value_range` and `nbins`.\n\n  Args:\n    values:  Numeric `Tensor`.\n    value_range:  Shape [2] `Tensor` of same `dtype` as `values`.\n      values <= value_range[0] will be mapped to hist[0],\n      values >= value_range[1] will be mapped to hist[-1].\n    nbins:  Scalar `int32 Tensor`.  Number of histogram bins.\n    dtype:  dtype for returned histogram.\n    name:  A name for this operation (defaults to 'histogram_fixed_width').\n\n  Returns:\n    A 1-D `Tensor` holding histogram of values.\n\n  Raises:\n    TypeError: If any unsupported dtype is provided.\n    tf.errors.InvalidArgumentError: If value_range does not\n        satisfy value_range[0] < value_range[1].\n\n  Examples:\n\n  ```python\n  # Bins will be:  (-inf, 1), [1, 2), [2, 3), [3, 4), [4, inf)\n  nbins = 5\n  value_range = [0.0, 5.0]\n  new_values = [-1.0, 0.0, 1.5, 2.0, 5.0, 15]\n\n  with tf.compat.v1.get_default_session() as sess:\n    hist = tf.histogram_fixed_width(new_values, value_range, nbins=5)\n    variables.global_variables_initializer().run()\n    sess.run(hist) => [2, 1, 1, 0, 2]\n  ```\n  "
    with ops.name_scope(name, 'histogram_fixed_width', [values, value_range, nbins]) as name:
        return gen_math_ops._histogram_fixed_width(values, value_range, nbins, dtype=dtype, name=name)