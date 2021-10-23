def _run(self):
    (xs_backward, y_backward, y0_data, y_grad) = self._forward_for_backward_gradients()
    self.y_grad = y_grad
    directions = self._sample_directions()
    gx_backward = self._directional_backward_gradients(xs_backward, y_backward, directions)
    if ((len(self.x_data) + len(self.params)) == self.no_grads.count(True)):
        return
    gx_numeric = self._directional_numeric_gradients(directions, y0_data)
    self._compare_gradients(gx_numeric, gx_backward, directions)