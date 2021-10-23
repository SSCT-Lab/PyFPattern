@tf_export(v1=['nn.softmax', 'math.softmax'])
@deprecation.deprecated_args(None, 'dim is deprecated, use axis instead', 'dim')
def softmax(logits, axis=None, name=None, dim=None):
    'Computes softmax activations.\n\n  This function performs the equivalent of\n\n      softmax = tf.exp(logits) / tf.reduce_sum(tf.exp(logits), axis)\n\n  See: https://en.wikipedia.org/wiki/Softmax_function\n\n  Example usage:\n  >>> tf.nn.softmax([-1, 0., 1.])\n  <tf.Tensor: shape=(3,), dtype=float32,\n  numpy=array([0.09003057, 0.24472848, 0.66524094], dtype=float32)>\n\n  Args:\n    logits: A non-empty `Tensor`. Must be one of the following types: `half`,\n      `float32`, `float64`.\n    axis: The dimension softmax would be performed on. The default is -1 which\n      indicates the last dimension.\n    name: A name for the operation (optional).\n    dim: Deprecated alias for `axis`.\n\n  Returns:\n    A `Tensor`. Has the same type and shape as `logits`.\n\n  Raises:\n    InvalidArgumentError: if `logits` is empty or `axis` is beyond the last\n      dimension of `logits`.\n  '
    axis = deprecation.deprecated_argument_lookup('axis', axis, 'dim', dim)
    if (axis is None):
        axis = (- 1)
    return _softmax(logits, gen_nn_ops.softmax, axis, name)