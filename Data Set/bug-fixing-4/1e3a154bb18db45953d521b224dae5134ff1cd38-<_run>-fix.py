def _run(self):
    (xs_backward, ys, params_backward) = self._forward_for_backward_gradients()
    ys0 = tuple([(None if (y is None) else y.array) for y in ys])
    if (self.gys is None):
        if (not ((len(ys) == 1) and (ys[0].shape == ()))):
            raise ValueError('y_grad argument cannot be omitted if the target function is not a loss function, which has a single output with shape ().\nActual output shapes: {}'.format(', '.join([str(y.shape) for y in ys])))
        self.gys = tuple([_ones_like(y.array) for y in ys])
    else:
        _check_outputs_and_grad_outputs(ys, self.gys)
    self.gys = tuple([(None if (y is None) else gy) for (gy, y) in zip(self.gys, ys0)])
    directions = self._sample_directions()
    gx_backward = self._directional_backward_gradients(xs_backward, ys, params_backward, directions)
    gx_numeric = self._directional_numeric_gradients(directions, ys0)
    self._compare_gradients(gx_numeric, gx_backward, directions)