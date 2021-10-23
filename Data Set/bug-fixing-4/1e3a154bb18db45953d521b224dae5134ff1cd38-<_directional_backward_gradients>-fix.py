def _directional_backward_gradients(self, xs, ys, params, directions):
    no_gxs = self.no_gxs
    y_backward = _apply_grad_setter_func(ys, [(None if (gy is None) else chainer.Variable(gy.copy(), requires_grad=False)) for gy in self.gys])
    y_backward.backward()
    for (no_gx, x) in six.moves.zip(no_gxs, xs):
        if (no_gx and (x.grad is not None)):
            raise RuntimeError('gradient of int variable must be None')
    grads = ([x.grad for (x, no_gx) in six.moves.zip(xs, no_gxs) if (not no_gx)] + [p.grad for p in params])
    gx_accum = 0
    assert (len(grads) == len(directions))
    for (g, direction) in six.moves.zip(grads, directions):
        if (g is not None):
            gx_accum += (g.astype(numpy.float64) * direction).sum()
    return gx_accum