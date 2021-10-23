

def batch_dot(x, y, axes=None):
    "Batchwise dot product.\n\n    `batch_dot` is used to compute dot product of `x` and `y` when\n    `x` and `y` are data in batch, i.e. in a shape of\n    `(batch_size, :)`.\n    `batch_dot` results in a tensor or variable with less dimensions\n    than the input. If the number of dimensions is reduced to 1,\n    we use `expand_dims` to make sure that ndim is at least 2.\n\n    # Arguments\n        x: Keras tensor or variable with `ndim >= 2`.\n        y: Keras tensor or variable with `ndim >= 2`.\n        axes: list of (or single) int with target dimensions.\n            The lengths of `axes[0]` and `axes[1]` should be the same.\n\n    # Returns\n        A tensor with shape equal to the concatenation of `x`'s shape\n        (less the dimension that was summed over) and `y`'s shape\n        (less the batch dimension and the dimension that was summed over).\n        If the final rank is 1, we reshape it to `(batch_size, 1)`.\n\n    # Examples\n        Assume `x = [[1, 2], [3, 4]]` and `y = [[5, 6], [7, 8]]`\n        `batch_dot(x, y, axes=1) = [[17], [53]]` which is the main diagonal\n        of `x.dot(y.T)`, although we never have to calculate the off-diagonal\n        elements.\n\n        Shape inference:\n        Let `x`'s shape be `(100, 20)` and `y`'s shape be `(100, 30, 20)`.\n        If `axes` is (1, 2), to find the output shape of resultant tensor,\n            loop through each dimension in `x`'s shape and `y`'s shape:\n\n        * `x.shape[0]` : 100 : append to output shape\n        * `x.shape[1]` : 20 : do not append to output shape,\n            dimension 1 of `x` has been summed over. (`dot_axes[0]` = 1)\n        * `y.shape[0]` : 100 : do not append to output shape,\n            always ignore first dimension of `y`\n        * `y.shape[1]` : 30 : append to output shape\n        * `y.shape[2]` : 20 : do not append to output shape,\n            dimension 2 of `y` has been summed over. (`dot_axes[1]` = 2)\n        `output_shape` = `(100, 30)`\n\n    ```python\n        >>> x_batch = K.ones(shape=(32, 20, 1))\n        >>> y_batch = K.ones(shape=(32, 30, 20))\n        >>> xy_batch_dot = K.batch_dot(x_batch, y_batch, axes=[1, 2])\n        >>> K.int_shape(xy_batch_dot)\n        (32, 1, 30)\n    ```\n    "
    if isinstance(axes, int):
        axes = (axes, axes)
    x_ndim = ndim(x)
    y_ndim = ndim(y)
    if (x_ndim > y_ndim):
        diff = (x_ndim - y_ndim)
        y = tf.reshape(y, tf.concat([tf.shape(y), ([1] * diff)], axis=0))
    elif (y_ndim > x_ndim):
        diff = (y_ndim - x_ndim)
        x = tf.reshape(x, tf.concat([tf.shape(x), ([1] * diff)], axis=0))
    else:
        diff = 0
    if ((ndim(x) == 2) and (ndim(y) == 2)):
        if (axes[0] == axes[1]):
            out = tf.reduce_sum(tf.multiply(x, y), axes[0])
        else:
            out = tf.reduce_sum(tf.multiply(tf.transpose(x, [1, 0]), y), axes[1])
    else:
        if (axes is not None):
            adj_x = (None if (axes[0] == (ndim(x) - 1)) else True)
            adj_y = (True if (axes[1] == (ndim(y) - 1)) else None)
        else:
            adj_x = None
            adj_y = None
        out = tf.matmul(x, y, adjoint_a=adj_x, adjoint_b=adj_y)
    if diff:
        if (x_ndim > y_ndim):
            idx = ((x_ndim + y_ndim) - 3)
        else:
            idx = (x_ndim - 1)
        out = tf.squeeze(out, list(range(idx, (idx + diff))))
    if (ndim(out) == 1):
        out = expand_dims(out, 1)
    return out
