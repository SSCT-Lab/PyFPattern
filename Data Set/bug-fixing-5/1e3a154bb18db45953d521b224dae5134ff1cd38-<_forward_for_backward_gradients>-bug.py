def _forward_for_backward_gradients(self):
    func = self.func
    x_data = self.x_data
    params = self.params
    xs = [variable.Variable(x, requires_grad=(x.dtype.kind == 'f')) for x in x_data]
    if self.is_immutable_params:
        params = tuple([chainer.Parameter(p) for p in params])
        y = func(xs, params)
    else:
        y = func(*xs)
    y = _as_tuple(y)
    self._clear_grads(xs)
    self._clear_grads(params)
    return (xs, y, params)