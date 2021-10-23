def _forward_for_backward_gradients(self):
    func = self.func
    xs = self.xs
    params = self.params
    xs = [variable.Variable(x, requires_grad=(x.dtype.kind == 'f')) for x in xs]
    if self.is_immutable_params:
        params = tuple([chainer.Parameter(p) for p in params])
        ys = func(xs, params)
    else:
        ys = func(*xs)
    ys = _as_tuple(ys)
    self._clear_grads(xs)
    self._clear_grads(params)
    return (xs, ys, params)