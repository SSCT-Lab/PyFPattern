def check_double_backward(func, x_data, y_grad, x_grad_grad, params=(), params_grad_grad=(), eps=0.001, atol=0.0001, rtol=0.001, no_grads=None, dtype=None, detect_nondifferentiable=False):
    'Test twice differentiation of a given procedure.\n\n    This function automatically checks if the backward procedure of ``func``\n    is correctly implemented for further differentiation. It first computes the\n    gradient of ``func`` w.r.t. its inputs in the same way as\n    :func:`~chainer.gradient_check.check_backward`. This function then further\n    invokes the backward procedure against the gradient variables, starting\n    from the initial gradient given by ``x_grad_grad``. It also computes the\n    second gradient using :func:`~chainer.gradient_check.numerical_grad`. The\n    resulting gradients are compared to confirm if the second-order gradients\n    are approximately correct.\n\n    Note that this function **DOES NOT** check if the first-order\n    differentiation is correct; the numerical gradient assumes that the\n    first-order gradient given by the usual :meth:`chainer.Variable.backward`\n    is correct. The implementation of each differentiable function should be\n    tested by :func:`~chainer.gradient_check.check_backward` first, and then\n    should be tested by this function if neccessary.\n\n    For the details of the arguments, see\n    :func:`~chainer.gradient_check.check_backward`. The additional arguments\n    ``x_grad_grad`` and ``params_grad_grad`` are (tuples of)\n    :class:`~chainer.Variable` (s) that include the initial gradient\n    corresponding to the first-order gradient of each input and parameter. Note\n    that the default error tolerance ``atol`` and ``rtol`` are slightly larger\n    than those of :func:`~chainer.gradient_check.check_backward` because the\n    numerical gradients of the second order differentiation are less accurate\n    than those of the first order gradients.\n\n    '
    xs = x_data
    gys = y_grad
    ggxs = x_grad_grad
    ggparams = params_grad_grad
    no_gxs = no_grads
    del x_data
    del y_grad
    del x_grad_grad
    del params_grad_grad
    del no_grads
    xs = _as_tuple(xs)
    params = _as_tuple(params)
    gys = _as_tuple(gys)
    ggxs = _as_tuple(ggxs)
    ggparams = _as_tuple(ggparams)
    n_x = len(xs)
    first_order_no_gxs = [(x.dtype.kind != 'f') for x in xs]

    def first_order_grad(*inputs):
        xs = inputs[:n_x]
        gys = inputs[n_x:]
        ys = _as_tuple(func(*xs))
        _check_outputs_and_grad_outputs(ys, gys)
        y_backward = _apply_grad_setter_func(ys, gys)
        y_backward.backward(enable_double_backprop=True)
        gxs = []
        errors = []
        for (i, (no_gx, x)) in enumerate(six.moves.zip(first_order_no_gxs, xs)):
            if no_gx:
                if (x.grad is not None):
                    errors.append('[{}]: Gradient was calculated while expected to not.'.format(i))
            elif (x.grad is None):
                gxs.append(None)
            else:
                gxs.append(x.grad_var)
        if (len(errors) > 0):
            f = six.StringIO()
            f.write('There are errors retrieving first-order gradients:\n')
            f.write('Inputs: {}\n'.format(utils._format_array_props(xs)))
            f.write('Skip: {}\n'.format(', '.join((str(no_gx) for no_gx in first_order_no_gxs))))
            f.write('Errors:\n')
            for error in errors:
                f.write('{}\n'.format(error))
            raise RuntimeError(f.getvalue())
        return tuple((gxs + [p.grad_var for p in params]))
    inputs = (xs + gys)
    grad_grad = (ggxs + ggparams)
    try:
        check_backward(first_order_grad, inputs, grad_grad, params=params, eps=eps, atol=atol, rtol=rtol, no_grads=no_gxs, dtype=dtype, detect_nondifferentiable=detect_nondifferentiable)
    except AssertionError as e:
        f = six.StringIO()
        f.write('check_double_backward failed (eps={} atol={} rtol={})\n'.format(eps, atol, rtol))
        for (i, x) in enumerate(xs):
            f.write('input[{}]:\n'.format(i))
            f.write('{}\n'.format(x))
        for (i, gy) in enumerate(gys):
            f.write('grad_output[{}]:\n'.format(i))
            f.write('{}\n'.format(gy))
        for (i, ggx) in enumerate(ggxs):
            f.write('grad_grad_input[{}]:\n'.format(i))
            f.write('{}\n'.format(ggx))
        for (i, ggp) in enumerate(ggparams):
            f.write('grad_grad_param[{}]:\n'.format(i))
            f.write('{}\n'.format(ggp))
        f.write('\n')
        f.write(str(e))
        utils._raise_from(AssertionError, f.getvalue(), e)