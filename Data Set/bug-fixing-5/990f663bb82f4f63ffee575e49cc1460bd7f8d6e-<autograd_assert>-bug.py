def autograd_assert(*args, **kwargs):
    f = kwargs['func']
    grad_f = kwargs['grad_func']
    grad_func = grad_and_loss(f)
    (grad_vals, output) = grad_func(*args)
    res = f(*args)
    assert (output == res)
    grad_res = grad_f(*args)
    assert (len(grad_vals) == len(grad_res))
    for (a, b) in zip(grad_vals, grad_res):
        assert (a == b)