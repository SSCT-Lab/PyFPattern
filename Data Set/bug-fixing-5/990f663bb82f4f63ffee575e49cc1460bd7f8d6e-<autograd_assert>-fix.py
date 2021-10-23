def autograd_assert(*args, **kwargs):
    f = kwargs['func']
    grad_f = kwargs['grad_func']
    grad_func = grad_and_loss(f)
    (grad_vals, output) = grad_func(*args)
    res = f(*args)
    assert same(output.asnumpy(), res.asnumpy())
    grad_res = grad_f(*args)
    assert (len(grad_vals) == len(grad_res))
    for (a, b) in zip(grad_vals, grad_res):
        assert same(a.asnumpy(), b.asnumpy())