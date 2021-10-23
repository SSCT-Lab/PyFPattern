def _run(self):
    (xs_backward, ys) = self._forward_for_backward_gradients()
    y0_data = tuple([y.array for y in ys])
    if (self.y_grad is None):
        if (not ((len(ys) == 1) and (ys[0].shape == ()))):
            raise ValueError('y_grad argument cannot be omitted if the target function is not a loss function, which has a single output with shape ().\nActual output shapes: {}'.format(', '.join([str(y.shape) for y in ys])))
        self.y_grad = tuple([_ones_like(y.array) for y in ys])
    else:
        _check_outputs_and_grad_outputs(ys, self.y_grad)
    directions = self._sample_directions()
    gx_backward = self._directional_backward_gradients(xs_backward, ys, directions)
    gx_numeric = self._directional_numeric_gradients(directions, y0_data)
    self._compare_gradients(gx_numeric, gx_backward, directions)