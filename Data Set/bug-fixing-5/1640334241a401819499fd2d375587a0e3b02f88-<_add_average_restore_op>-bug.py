def _add_average_restore_op(self, block, param_grad):
    param = block.clone_variable(param_grad[0])
    grad = block.clone_variable(param_grad[1])
    layers.assign(input=grad, output=param)