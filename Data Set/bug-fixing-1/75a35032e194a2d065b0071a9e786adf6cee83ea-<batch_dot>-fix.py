

def batch_dot(x, y, axes=None):
    "Batchwise dot product.\n\n    `batch_dot` is used to compute dot product of `x` and `y` when\n    `x` and `y` are data in batches, i.e. in a shape of\n    `(batch_size, :)`.\n    `batch_dot` results in a tensor or variable with less dimensions\n    than the input. If the number of dimensions is reduced to 1,\n    we use `expand_dims` to make sure that ndim is at least 2.\n\n    # Arguments\n        x: Keras tensor or variable with `ndim >= 2`.\n        y: Keras tensor or variable with `ndim >= 2`.\n        axes: int or tuple(int, int). Target dimensions to be reduced.\n\n    # Returns\n        A tensor with shape equal to the concatenation of `x`'s shape\n        (less the dimension that was summed over) and `y`'s shape\n        (less the batch dimension and the dimension that was summed over).\n        If the final rank is 1, we reshape it to `(batch_size, 1)`.\n\n    # Examples\n        Assume `x = [[1, 2], [3, 4]]` and `y = [[5, 6], [7, 8]]`\n        `batch_dot(x, y, axes=1) = [[17], [53]]` which is the main diagonal\n        of `x.dot(y.T)`, although we never have to calculate the off-diagonal\n        elements.\n\n        Pseudocode:\n        ```\n        inner_products = []\n        for xi, yi in zip(x, y):\n            inner_products.append(xi.dot(yi))\n        result = stack(inner_products)\n        ```\n\n        Shape inference:\n        Let `x`'s shape be `(100, 20)` and `y`'s shape be `(100, 30, 20)`.\n        If `axes` is (1, 2), to find the output shape of resultant tensor,\n            loop through each dimension in `x`'s shape and `y`'s shape:\n\n        * `x.shape[0]` : 100 : append to output shape\n        * `x.shape[1]` : 20 : do not append to output shape,\n            dimension 1 of `x` has been summed over. (`dot_axes[0]` = 1)\n        * `y.shape[0]` : 100 : do not append to output shape,\n            always ignore first dimension of `y`\n        * `y.shape[1]` : 30 : append to output shape\n        * `y.shape[2]` : 20 : do not append to output shape,\n            dimension 2 of `y` has been summed over. (`dot_axes[1]` = 2)\n        `output_shape` = `(100, 30)`\n\n    ```python\n        >>> x_batch = K.ones(shape=(32, 20, 1))\n        >>> y_batch = K.ones(shape=(32, 30, 20))\n        >>> xy_batch_dot = K.batch_dot(x_batch, y_batch, axes=(1, 2))\n        >>> K.int_shape(xy_batch_dot)\n        (32, 1, 30)\n    ```\n\n    {{np_implementation}}\n    "
    x_shape = int_shape(x)
    y_shape = int_shape(y)
    x_ndim = len(x_shape)
    y_ndim = len(y_shape)
    if ((x_ndim < 2) or (y_ndim < 2)):
        raise ValueError((((('Can not do batch_dot on inputs with rank < 2. Received inputs with shapes ' + str(x_shape)) + ' and ') + str(y_shape)) + '.'))
    x_batch_size = x_shape[0]
    y_batch_size = y_shape[0]
    if ((x_batch_size is not None) and (y_batch_size is not None)):
        if (x_batch_size != y_batch_size):
            raise ValueError((((('Can not do batch_dot on inputs with different batch sizes. Received inputs with shapes ' + str(x_shape)) + ' and ') + str(y_shape)) + '.'))
    if isinstance(axes, int):
        axes = [axes, axes]
    if (axes is None):
        if (y_ndim == 2):
            axes = [(x_ndim - 1), (y_ndim - 1)]
        else:
            axes = [(x_ndim - 1), (y_ndim - 2)]
    if py_any([isinstance(a, (list, tuple)) for a in axes]):
        raise ValueError(((('Multiple target dimensions are not supported. ' + 'Expected: None, int, (int, int), ') + 'Provided: ') + str(axes)))
    axes = list(axes)
    if (axes[0] < 0):
        axes[0] += x_ndim
    if (axes[1] < 0):
        axes[1] += y_ndim
    if (0 in axes):
        raise ValueError('Can not perform batch_dot over axis 0.If your inputs are not batched, add a dummy batch dimension to your inputs using K.expand_dims(x, 0)')
    (a0, a1) = axes
    d1 = x_shape[a0]
    d2 = y_shape[a1]
    if ((d1 is not None) and (d2 is not None) and (d1 != d2)):
        raise ValueError((((((('Can not do batch_dot on inputs with shapes ' + str(x_shape)) + ' and ') + str(y_shape)) + ' with axes=') + str(axes)) + ('. x.shape[%d] != y.shape[%d] (%d != %d).' % (axes[0], axes[1], d1, d2))))
    if (a0 != 1):
        pattern = list(range(x_ndim))
        for i in range(a0, 1, (- 1)):
            pattern[i] = pattern[(i - 1)]
        pattern[1] = a0
        x = permute_dimensions(x, pattern)
    if (a1 != 1):
        pattern = list(range(y_ndim))
        for i in range(a1, 1, (- 1)):
            pattern[i] = pattern[(i - 1)]
        pattern[1] = a1
        y = permute_dimensions(y, pattern)
    x_shape = tf.shape(x)
    y_shape = tf.shape(y)
    new_x_shape = tf.concat([x_shape, tf.ones_like(y_shape[2:])], 0)
    new_y_shape = tf.concat([y_shape[:2], tf.ones_like(x_shape[2:]), y_shape[2:]], 0)
    x = reshape(x, new_x_shape)
    y = reshape(y, new_y_shape)
    result = tf.reduce_sum((x * y), 1)
    if (ndim(result) == 1):
        result = tf.expand_dims(result, (- 1))
    return result
