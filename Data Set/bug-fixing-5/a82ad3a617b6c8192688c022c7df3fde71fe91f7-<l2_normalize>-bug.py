def l2_normalize(x, axis=None):
    'Normalizes a tensor wrt the L2 norm alongside the specified axis.\n\n    # Arguments\n        x: Tensor or variable.\n        axis: axis along which to perform normalization.\n\n    # Returns\n        A tensor.\n    '
    return tf.nn.l2_normalize(x, dim=axis)