@ops.RegisterGradient('NcclReduce')
def _reduce_sum_grad(op, grad):
    'The gradients for input `Operation` of `reduce_sum`.\n\n  Args:\n    op: The `sum send` `Operation` that we are differentiating.\n    grad: Gradient with respect to the output of the `reduce_sum` op.\n\n  Returns:\n    The gradient with respect to the input of `reduce_sum` op.\n\n  Raises:\n    LookupError: If the reduction attribute of op is not `sum`.\n  '
    if (op.get_attr('reduction') != b'sum'):
        raise LookupError('No gradient defined for NcclReduce except sum.')
    _check_device(grad, expected=op.device)
    with ops.device(op.device):
        result = gen_nccl_ops.nccl_broadcast(input=grad, shape=grad.shape)
    return ([result] * len(op.inputs))