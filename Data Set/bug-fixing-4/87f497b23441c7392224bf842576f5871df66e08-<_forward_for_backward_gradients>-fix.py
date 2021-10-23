def _forward_for_backward_gradients(self):
    func = self.func
    x_data = self.x_data
    params = self.params
    xs = [variable.Variable(x) for x in x_data]
    y = func(*xs)
    y = _as_tuple(y)
    self._clear_grads(xs)
    self._clear_grads(params)
    return (xs, y)