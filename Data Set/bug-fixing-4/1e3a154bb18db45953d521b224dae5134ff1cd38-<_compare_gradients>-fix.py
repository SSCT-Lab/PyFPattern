def _compare_gradients(self, gx_numeric, gx_backward, directions):
    atol = self.atol
    rtol = self.rtol
    try:
        testing.assert_allclose(gx_numeric, gx_backward, atol=atol, rtol=rtol)
    except AssertionError as e:
        eps = self.eps
        xs = self.xs
        gys = self.gys
        f = six.StringIO()
        f.write('check_backward failed (eps={} atol={} rtol={})\n'.format(eps, atol, rtol))
        for (i, x) in enumerate(xs):
            f.write('inputs[{}]:\n'.format(i))
            f.write('{}\n'.format(x))
        for (i, gy) in enumerate(gys):
            f.write('grad_outputs[{}]:\n'.format(i))
            f.write('{}\n'.format(gy))
        for (i, d) in enumerate(directions):
            f.write('directions[{}]:\n'.format(i))
            f.write('{}\n'.format(d))
        f.write('gradients (numeric):  {}\n'.format(gx_numeric))
        f.write('gradients (backward): {}\n'.format(gx_backward))
        f.write('\n')
        f.write('x: numeric gradient, y: backward gradient')
        f.write(str(e))
        raise AssertionError(f.getvalue())