

def sparse_categorical_crossentropy(output, target, from_logits=False):
    'Categorical crossentropy between an output tensor\n    and a target tensor, where the target is an integer tensor.\n    '
    if (not from_logits):
        epsilon = _to_tensor(_EPSILON, output.dtype.base_dtype)
        output = tf.clip_by_value(output, epsilon, (1 - epsilon))
        output = tf.log(output)
    output_shape = output.get_shape()
    res = tf.nn.sparse_softmax_cross_entropy_with_logits(tf.reshape(output, [(- 1), int(output_shape[(- 1)])]), cast(flatten(target), 'int64'))
    if (len(output_shape) == 3):
        return tf.reshape(res, [(- 1), int(output_shape[(- 2)])])
    else:
        return res
