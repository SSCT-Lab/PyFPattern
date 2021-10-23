

def _softmax(logits, compute_op, dim=(- 1), name=None):
    'Helper function for softmax and log_softmax.\n\n  It reshapes and transposes the input logits into a 2-D Tensor and then invokes\n  the tf.nn._softmax or tf.nn._log_softmax function. The output would be\n  transposed and reshaped back.\n\n  Args:\n    logits: A non-empty `Tensor`. Must be one of the following types: `half`,\n      `float32`, `float64`.\n    compute_op: Either gen_nn_ops.softmax or gen_nn_ops.log_softmax\n    dim: The dimension softmax would be performed on. The default is -1 which\n      indicates the last dimension.\n    name: A name for the operation (optional).\n\n  Returns:\n    A `Tensor`. Has the same type as `logits`. Same shape as `logits`.\n  Raises:\n    InvalidArgumentError: if `logits` is empty or `dim` is beyond the last\n      dimension of `logits`.\n  '

    def _swap_axis(logits, dim_index, last_index, name=None):
        "Swaps logits's dim_index and last_index."
        return array_ops.transpose(logits, array_ops.concat([math_ops.range(dim_index), [last_index], math_ops.range((dim_index + 1), last_index), [dim_index]], 0), name=name)
    logits = ops.convert_to_tensor(logits)
    shape = logits.get_shape()
    is_last_dim = ((dim is (- 1)) or (dim == (shape.ndims - 1)))
    if is_last_dim:
        return compute_op(logits, name=name)
    dim_val = dim
    if isinstance(dim, ops.Tensor):
        dim_val = tensor_util.constant_value(dim)
    if ((dim_val is not None) and ((dim_val < (- shape.ndims)) or (dim_val >= shape.ndims))):
        raise errors_impl.InvalidArgumentError(None, None, ('Dimension (%d) must be in the range [%d, %d) where %d is the number of dimensions in the input.' % (dim_val, (- shape.ndims), shape.ndims, shape.ndims)))
    ndims = array_ops.rank(logits)
    if (not isinstance(dim, ops.Tensor)):
        if (dim < 0):
            dim += ndims
    else:
        dim = array_ops.where(math_ops.less(dim, 0), (dim + ndims), dim)
    input_rank = array_ops.rank(logits)
    dim_axis = (dim % shape.ndims)
    logits = _swap_axis(logits, dim_axis, math_ops.subtract(input_rank, 1))
    output = compute_op(logits)
    output = _swap_axis(output, dim_axis, math_ops.subtract(input_rank, 1), name=name)
    output.set_shape(shape)
    return output
