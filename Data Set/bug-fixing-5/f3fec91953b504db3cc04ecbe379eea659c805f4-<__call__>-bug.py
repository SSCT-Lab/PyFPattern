def __call__(self, rule, param):
    grad = param.grad
    if (grad is None):
        return
    with chainer.using_device(param.device):
        xp = param.device.xp
        if ((xp == backend.chainerx) or isinstance(param.grad, backend.intel64.mdarray)):
            grad[:] = grad.clip(self.lower_bound, self.upper_bound)
        else:
            xp.clip(grad, self.lower_bound, self.upper_bound, out=grad)