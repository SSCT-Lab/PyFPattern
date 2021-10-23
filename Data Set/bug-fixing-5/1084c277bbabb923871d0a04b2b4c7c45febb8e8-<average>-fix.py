def average(x, axis=None, weights=None, keepdims=False):
    'Calculate weighted average of array elements over a given axis.\n\n    Args:\n        x (:class:`~chainer.Variable` or :ref:`ndarray`): Elements to sum.\n        axis (None or int or tuple of int): Axis which the method is performed.\n            With the default (axis = None) it performs a mean over all the\n            dimensions of the input array.\n        weights (None or :class:`~chainer.Variable` or :ref:`ndarray`):\n            An array holding weights to calculate weighted average.\n            If it is ``None``, all weights are assumed to be one.\n            When ``axis`` is ``None``, ``weights`` must have the same shape\n            of ``x``. And when ``axis`` is ``int``, it must be 1-D array\n            satisfying ``weights.shape == (x.shape[axis],)``.\n        keepdims (bool): If ``True``, the specified axes are remained as axes\n            of length one.\n\n    Returns:\n        ~chainer.Variable: Output variable.\n\n    '
    if (axis is None):
        pass
    elif isinstance(axis, tuple):
        axis = [((a + x.ndim) if (a < 0) else a) for a in axis]
        axis.sort()
        for (a, b) in six.moves.zip(axis, axis[1:]):
            if (a == b):
                raise ValueError("duplicate value in 'axis'")
        axis = tuple(axis)
    else:
        if (axis < 0):
            axis += x.ndim
        axis = (axis,)
    if (weights is not None):
        if ((axis is not None) and (len(axis) > 1)):
            raise ValueError('tuple axis is not supported when weights is given')
        divider = sum_mod.sum(weights)
        if (axis is not None):
            w_shape = [(d if (i in axis) else 1) for (i, d) in enumerate(x.shape)]
            weights = broadcast.broadcast_to(reshape.reshape(weights, w_shape), x.shape)
        x = (x * weights)
    elif (axis is None):
        divider = x.size
    else:
        divider = 1
        for a in axis:
            divider *= x.shape[a]
    x_sum = sum_mod.sum(x, axis, keepdims)
    if (weights is not None):
        divider = broadcast.broadcast_to(divider, x_sum.shape)
    return (x_sum / divider)