def _directional_backward_gradients(self, xs, y, directions):
    params = self.params
    no_grads = self.no_grads
    y.backward()
    for (no_grad, x) in six.moves.zip(no_grads, xs):
        if (no_grad and (x.grad is not None)):
            raise RuntimeError('gradient of int variable must be None')
    grads = ([x.grad for (x, no_grad) in six.moves.zip(xs, no_grads) if (not no_grad)] + [p.grad for p in params])
    gx_accum = 0
    assert (len(grads) == len(directions))
    for (g, direction) in six.moves.zip(grads, directions):
        if (g is not None):
            gx_accum += (g.astype(numpy.float64) * direction).sum()
    return gx_accum