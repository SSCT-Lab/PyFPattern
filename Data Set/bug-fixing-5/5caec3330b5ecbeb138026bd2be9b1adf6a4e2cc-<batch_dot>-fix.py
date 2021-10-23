def batch_dot(x, y, axes=None):
    "Batchwise dot product.\n\n    batch_dot results in a tensor with less dimensions than the input.\n    If the number of dimensions is reduced to 1, we use `expand_dims` to\n    make sure that ndim is at least 2.\n\n    # Arguments\n        x, y: tensors with ndim >= 2\n        axes: list (or single) int with target dimensions\n\n    # Returns\n        A tensor with shape equal to the concatenation of x's shape\n        (less the dimension that was summed over) and y's shape\n        (less the batch dimension and the dimension that was summed over).\n        If the final rank is 1, we reshape it to (batch_size, 1).\n\n    # Examples\n        Assume x = [[1, 2], [3, 4]]   and y = [[5, 6], [7, 8]]\n        batch_dot(x, y, axes=1) = [[17, 53]] which is the main diagonal\n        of x.dot(y.T), although we never have to calculate the off-diagonal\n        elements.\n\n        Shape inference:\n        Let x's shape be (100, 20) and y's shape be (100, 30, 20).\n        If dot_axes is (1, 2), to find the output shape of resultant tensor,\n            loop through each dimension in x's shape and y's shape:\n        x.shape[0] : 100 : append to output shape\n        x.shape[1] : 20 : do not append to output shape,\n            dimension 1 of x has been summed over. (dot_axes[0] = 1)\n        y.shape[0] : 100 : do not append to output shape,\n            always ignore first dimension of y\n        y.shape[1] : 30 : append to output shape\n        y.shape[2] : 20 : do not append to output shape,\n            dimension 2 of y has been summed over. (dot_axes[1] = 2)\n\n        output_shape = (100, 30)\n    "
    if isinstance(axes, int):
        axes = (axes, axes)
    if (axes is None):
        axes = [(x.ndim - 1), (y.ndim - 2)]
    if isinstance(axes, tuple):
        axes = list(axes)
    if (axes[0] == 0):
        x = transpose(x)
        axes[0] = (x.ndim - 1)
    if (axes[1] == 0):
        y = transpose(y)
        axes[1] = (y.ndim - 1)
    out = T.batched_tensordot(x, y, axes=axes)
    if (ndim(out) == 1):
        out = expand_dims(out, 1)
    if (hasattr(x, '_keras_shape') and hasattr(y, '_keras_shape')):
        shape = []
        for axis in range(len(x._keras_shape)):
            if (axis != axes[0]):
                shape.append(x._keras_shape[axis])
        for axis in range(1, len(y._keras_shape)):
            if (axis != axes[1]):
                shape.append(y._keras_shape[axis])
        if (len(shape) == 1):
            shape.append(1)
        out._keras_shape = tuple(shape)
    return out