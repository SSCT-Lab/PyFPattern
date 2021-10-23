def _do_backward(self, grad_output, retain_variables):
    if (not hasattr(self, 'saved_variables')):
        raise RuntimeError('Trying to backward through the graph second time, but the buffers have already been freed. Please specify retain_variables=True when calling backward for the first time.')
    grad_input = self.backward(*grad_output)
    if (not isinstance(grad_input, tuple)):
        grad_input = (grad_input,)
    assert (len(grad_input) == len(self.previous_functions)), (self.__class__.__name__ + ' returned an invalid number of gradient tensors')
    self._call_hooks(grad_input, grad_output)
    if (not retain_variables):
        del self.saved_variables
    return grad_input