

def batch_norm(input, running_mean, running_var, weight=None, bias=None, training=False, momentum=0.1, eps=1e-05):
    size = list(input.size())
    if (reduce(mul, size[2:], size[0]) == 1):
        raise ValueError('Expected more than 1 value per channel, got input size {}'.format(size))
    f = torch._C._functions.BatchNorm(running_mean, running_var, training, momentum, eps, torch.backends.cudnn.enabled)
    return f(input, weight, bias)
