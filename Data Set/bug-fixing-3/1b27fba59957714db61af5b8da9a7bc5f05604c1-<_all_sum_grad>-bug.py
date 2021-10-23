@ops.RegisterGradient('NcclAllReduce')
def _all_sum_grad(op, grad):
    'The gradients for `all_sum`.\n\n  Args:\n    op: The `all_sum` `Operation` that we are differentiating.\n    grad: Gradient with respect to the output of the `all_sum` op.\n\n  Returns:\n    The gradient with respect to the output of `all_sum`.\n\n  Raises:\n    LookupError: If `reduction` is not `sum`.\n  '
    if (op.get_attr('reduction') != 'sum'):
        raise LookupError('No gradient defined for NcclAllReduce except sum.')
    _check_device(grad, expected=op.device)
    num_devices = op.get_attr('num_devices')
    shared_name = (op.get_attr('shared_name') + '_grad')
    with ops.device(op.device):
        return gen_nccl_ops.nccl_all_reduce(input=grad, reduction='sum', num_devices=num_devices, shared_name=shared_name)