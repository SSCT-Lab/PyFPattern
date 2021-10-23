def batch_norm(input, running_mean, running_var, weight=None, bias=None, training=False, momentum=0.1, eps=1e-05):
    f = torch._C._functions.BatchNorm(running_mean, running_var, training, momentum, eps, torch.backends.cudnn.enabled)
    return f(input, weight, bias)