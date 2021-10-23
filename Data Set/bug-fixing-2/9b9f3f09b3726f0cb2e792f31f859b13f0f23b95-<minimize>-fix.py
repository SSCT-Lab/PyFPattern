

def minimize(self, loss, startup_program=None, parameter_list=None, no_grad_set=None):
    'Add operations to minimize `loss` by updating `parameter_list`.\n\n        This method combines interface `append_backward()` and\n        `create_optimization_pass()` into one.\n        '
    params_grads = append_backward(loss, parameter_list, no_grad_set, [error_clip_callback])
    params_grads = sorted(params_grads, key=(lambda x: x[0].name))
    params_grads = append_gradient_clip_ops(params_grads)
    params_grads = append_regularization_ops(params_grads, self.regularization)
    optimize_ops = self.create_optimization_pass(params_grads, loss, startup_program)
    return (optimize_ops, params_grads)
