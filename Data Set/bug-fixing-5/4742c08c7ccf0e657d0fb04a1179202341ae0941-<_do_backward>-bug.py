def _do_backward(self, grad_output, retain_variables):
    grad_input = self.backward(*grad_output)
    if (not isinstance(grad_input, tuple)):
        grad_input = (grad_input,)
    assert (len(grad_input) == len(self.previous_functions)), (self.__class__.__name__ + ' returned an invalid number of gradient tensors')
    self._call_hooks(grad_input, grad_output)
    if (not retain_variables):
        del self.saved_variables
    return grad_input