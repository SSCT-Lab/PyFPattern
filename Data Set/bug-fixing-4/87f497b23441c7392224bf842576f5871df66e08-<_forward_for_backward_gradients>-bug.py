def _forward_for_backward_gradients(self):
    func = self.func
    x_data = self.x_data
    y_grad = self.y_grad
    params = self.params
    xs = [variable.Variable(x) for x in x_data]
    y = func(*xs)
    y = _as_tuple(y)
    y0_data = [_.data for _ in y]
    (y, y_grad) = _set_y_grad(y, y_grad)
    self._clear_grads(xs)
    self._clear_grads(params)
    return (xs, y, y0_data, y_grad)