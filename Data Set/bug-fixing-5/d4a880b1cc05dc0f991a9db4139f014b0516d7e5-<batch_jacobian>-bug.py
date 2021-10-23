def batch_jacobian(self, target, source, unconnected_gradients=UnconnectedGradients.NONE, parallel_iterations=None, experimental_use_pfor=True):
    "Computes and stacks per-example jacobians.\n\n    See http://en.wikipedia.org/wiki/jacobian_matrix_and_determinant for the\n    definition of a Jacobian.  This function is essentially an efficient\n    implementation of the following:\n    `tf.stack([self.jacobian(y[i], x[i]) for i in range(x.shape[0])])`.\n\n    Note that compared to `GradientTape.jacobian` which computes gradient of\n    each output value w.r.t each input value, this function is useful when\n    `target[i,...] is independent of `source[j,...]` for `j != i`. This\n    independence assumption allows more efficient computation as compared to\n    `GradientTape.jacobian`. The output, as well as intermediate activations,\n    are lower dimensional and avoid a bunch of redundant zeros which would\n    result in the jacobian computation given the independence assumption.\n\n    Example usage:\n    ```python\n    with tf.GradientTape() as g:\n      x = tf.constant([[1, 2], [3, 4]], dtype=tf.float32)\n      g.watch(x)\n      y = x * x\n    batch_jacobian = g.batch_jacobian(y, x)\n    # batch_jacobian is [[[2,  0], [0,  4]], [[6,  0], [0,  8]]]\n    ```\n\n    Args:\n      target: A tensor with rank 2 or higher and with shape [b, y1, ..., y_n].\n        `target[i,...]` should only depend on `source[i,...]`.\n      source: A tensor with rank 2 or higher and with shape [b, x1, ..., x_m].\n      unconnected_gradients: a value which can either hold 'none' or 'zero' and\n        alters the value which will be returned if the target and sources are\n        unconnected. The possible values and effects are detailed in\n        'UnconnectedGradients' and it defaults to 'none'.\n      parallel_iterations: A knob to control how many iterations are dispatched\n        in parallel. This knob can be used to control the total memory usage.\n      experimental_use_pfor: If true, uses pfor for computing the Jacobian. Else\n        uses a tf.while_loop.\n\n    Returns:\n      A tensor `t` with shape [b, y_1, ..., y_n, x1, ..., x_m] where `t[i, ...]`\n      is the jacobian of `target[i, ...]` w.r.t. `source[i, ...]`, i.e. stacked\n      per-example jacobians.\n\n    Raises:\n      RuntimeError: If called on a non-persistent tape with eager execution\n        enabled and without enabling experimental_use_pfor.\n      ValueError: If vectorization of jacobian computation fails or if first\n        dimension of `target` and `source` do not match.\n    "
    target_shape = target.shape
    if (target_shape.rank is None):
        dim = tensor_shape.Dimension(None)
    else:
        dim = target_shape.dims[0]
    if (not (target_shape.with_rank_at_least(2) and source.shape.with_rank_at_least(2) and dim.is_compatible_with(source.shape[0]))):
        raise ValueError(('Need first dimension of target shape (%s) and source shape (%s) to match.' % (target.shape, source.shape)))
    if target_shape.is_fully_defined():
        batch_size = int(target_shape[0])
        target_row_size = (target_shape.num_elements() // batch_size)
    else:
        target_shape = array_ops.shape(target)
        batch_size = target_shape[0]
        target_row_size = (array_ops.size(target) // batch_size)
    source_shape = array_ops.shape(source)
    self._push_tape()
    with ops.control_dependencies([check_ops.assert_equal(batch_size, source_shape[0])]):
        target = array_ops.reshape(target, [batch_size, target_row_size])
    self._pop_tape()

    def loop_fn(i):
        self._push_tape()
        y = array_ops.gather(target, i, axis=1)
        self._pop_tape()
        return self.gradient(y, source, unconnected_gradients=unconnected_gradients)
    if experimental_use_pfor:
        try:
            output = pfor_ops.pfor(loop_fn, target_row_size, parallel_iterations=parallel_iterations)
        except ValueError as err:
            six.reraise(ValueError, ValueError((str(err) + '\nEncountered an exception while vectorizing the batch_jacobian computation. Vectorization can be disabled by setting experimental_use_pfor to False.')), sys.exc_info()[2])
    else:
        if (context.executing_eagerly() and (not self._persistent)):
            raise RuntimeError('GradientTape must be created with persistent=True to compute the batch_jacobian with eager execution enabled and  with experimental_use_pfor set to False.')
        output = pfor_ops.for_loop(loop_fn, target.dtype, target_row_size, parallel_iterations=parallel_iterations)
    if (output is None):
        return None
    output = array_ops.reshape(output, [target_row_size, batch_size, (- 1)])
    output = array_ops.transpose(output, [1, 0, 2])
    new_shape = array_ops.concat([target_shape, source_shape[1:]], axis=0)
    return array_ops.reshape(output, new_shape)