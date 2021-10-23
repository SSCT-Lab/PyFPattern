def _compare_gradients(self, gx_numeric, gx_backward, directions):
    atol = self.atol
    rtol = self.rtol
    try:
        testing.assert_allclose(gx_numeric, gx_backward, atol=atol, rtol=rtol)
    except AssertionError as e:
        eps = self.eps
        x_data = self.x_data
        y_grad = self.y_grad
        f = six.StringIO()
        f.write('check_backward failed (eps={} atol={} rtol={})\n'.format(eps, atol, rtol))
        for (i, x_) in enumerate(x_data):
            f.write('inputs[{}]:\n'.format(i))
            f.write('{}\n'.format(x_))
        for (i, gy_) in enumerate(y_grad):
            f.write('grad_outputs[{}]:\n'.format(i))
            f.write('{}\n'.format(gy_))
        for (i, d_) in enumerate(directions):
            f.write('directions[{}]:\n'.format(i))
            f.write('{}\n'.format(d_))
        f.write('gradients (numeric):  {}\n'.format(gx_numeric))
        f.write('gradients (backward): {}\n'.format(gx_backward))
        f.write('\n')
        f.write('x: numeric gradient, y: backward gradient')
        f.write(str(e))
        raise AssertionError(f.getvalue())