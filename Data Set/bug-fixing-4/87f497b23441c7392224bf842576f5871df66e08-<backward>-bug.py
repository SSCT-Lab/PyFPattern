def backward(self, indexes, grad_outputs):
    if (self.grad is None):
        grad = (self.xp.ones(self.input_shape, self.input_dtype),)
    else:
        grad = self.grad
    return tuple(((None if (g is None) else variable.as_variable(g)) for g in grad))