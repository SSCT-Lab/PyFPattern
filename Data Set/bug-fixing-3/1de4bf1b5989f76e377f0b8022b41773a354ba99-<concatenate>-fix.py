def concatenate(tensors, axis=(- 1)):
    'Concatenates a list of tensors alongside the specified axis.\n\n    # Returns\n        A tensor.\n    '
    if (axis < 0):
        dims = ndim(tensors[0])
        if dims:
            axis = (axis % dims)
        else:
            axis = 0
    if py_all([is_sparse(x) for x in tensors]):
        return tf.sparse_concat(axis, tensors)
    elif (tf_major_version >= 1):
        return tf.concat([to_dense(x) for x in tensors], axis)
    else:
        try:
            return tf.concat_v2([to_dense(x) for x in tensors], axis)
        except AttributeError:
            return tf.concat(axis, [to_dense(x) for x in tensors])