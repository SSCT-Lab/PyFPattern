def _add_average_restore_op(self, block, param_grad):
    param = block._clone_variable(param_grad[0])
    grad = block._clone_variable(param_grad[1])
    layers.assign(input=grad, output=param)