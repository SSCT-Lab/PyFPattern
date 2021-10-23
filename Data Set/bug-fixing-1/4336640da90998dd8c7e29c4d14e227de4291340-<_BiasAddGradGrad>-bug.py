

@ops.RegisterGradient('BiasAddGrad')
def _BiasAddGradGrad(op, received_grad):
    'Gradient for the BiasAddGrad op.\n\n  Args:\n    op: BiasAddGrad op for which we are calculating gradients.\n    received_grad: The gradients passed to the BiasAddGrad op.\n    \n  Returns:\n    A single gradient Tensor for the input to BiasAddGrad (which\n    is the gradient of the bias term in BiasAdd)\n  '
    try:
        data_format = op.get_attr('data_format')
    except ValueError:
        data_format = None
    shape = array_ops.shape(op.inputs[0])
    rank = array_ops.rank(op.inputs[0])
    bias_shape = array_ops.shape(received_grad)
    if (data_format == 'NCHW'):
        expanded_shape = array_ops.concat(0, [array_ops.ones_like(shape[:(- 3)]), bias_shape, array_ops.ones_like(shape[(- 2):])])
        tile_mults = array_ops.concat(0, [shape[:(- 3)], [1], shape[(- 2):]])
    else:
        expanded_shape = array_ops.concat(0, [array_ops.ones_like(shape[:(- 1)]), bias_shape])
        tile_mults = array_ops.concat(0, [shape[:(- 1)], [1]])
    expanded_grad = array_ops.reshape(received_grad, expanded_shape)
    return array_ops.tile(expanded_grad, tile_mults)
