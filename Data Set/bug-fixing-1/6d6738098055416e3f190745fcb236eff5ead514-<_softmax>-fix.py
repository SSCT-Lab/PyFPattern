

def _softmax(logits, compute_op, dim=(- 1), name=None):
    'Helper function for softmax and log_softmax.\n\n  It reshapes and transposes the input logits into a 2-D Tensor and then invokes\n  the tf.nn._softmax or tf.nn._log_softmax function. The output would be\n  transposed and reshaped back.\n\n  Args:\n    logits: A non-empty `Tensor`. Must be one of the following types: `half`,\n      `float32`, `float64`.\n    compute_op: Either gen_nn_ops._softmax or gen_nn_ops._log_softmax\n    dim: The dimension softmax would be performed on. The default is -1 which\n      indicates the last dimension.\n    name: A name for the operation (optional).\n\n  Returns:\n    A `Tensor`. Has the same type as `logits`. Same shape as `logits`.\n  Raises:\n    InvalidArgumentError: if `logits` is empty or `dim` is beyond the last\n      dimension of `logits`.\n  '

    def _swap_axis(logits, dim_index, last_index, name=None):
        "Swaps logits's dim_index and last_index."
        return array_ops.transpose(logits, array_ops.concat([math_ops.range(dim_index), [last_index], math_ops.range((dim_index + 1), last_index), [dim_index]], 0), name=name)
    logits = ops.convert_to_tensor(logits)
    shape = logits.get_shape()
    is_last_dim = ((dim is (- 1)) or (dim == (shape.ndims - 1)))
    if ((shape.ndims is 2) and is_last_dim):
        return compute_op(logits, name=name)
    if is_last_dim:
        input_shape = array_ops.shape(logits)
        logits = _flatten_outer_dims(logits)
        output = compute_op(logits)
        output = array_ops.reshape(output, input_shape, name=name)
        return output
    input_rank = array_ops.rank(logits)
    logits = _swap_axis(logits, dim, math_ops.subtract(input_rank, 1))
    shape_after_swap = array_ops.shape(logits)
    logits = _flatten_outer_dims(logits)
    output = compute_op(logits)
    output = array_ops.reshape(output, shape_after_swap)
    output = _swap_axis(output, dim, math_ops.subtract(input_rank, 1), name=name)
    output.set_shape(shape)
    return output
