def backward(self, out_grads=None):
    'Backward computation.'
    assert (self.binded and self.params_initialized)
    for (i_layer, module) in reversed(zip(range(len(self._modules)), self._modules)):
        module.backward(out_grads=out_grads)
        if (i_layer == 0):
            break
        out_grads = module.get_input_grads()