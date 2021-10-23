def check_backward(func, x_data, y_grad, params=(), eps=0.001, atol=1e-05, rtol=0.0001, no_grads=None, dtype=None):
    "Test backward procedure of a given function.\n\n    This function automatically checks backward-process of a given function.\n    For example, when you have a :class:`~chainer.Function` class ``MyFunc``,\n    that gets two arguments and returns one value, you can make its test like\n    this::\n\n    >> def test_my_func(self):\n    >>   func = MyFunc()\n    >>   x1_data = xp.array(...)\n    >>   x2_data = xp.array(...)\n    >>   gy_data = xp.array(...)\n    >>   check_backward(func, (x1_data, x2_data), gy_data)\n\n    This method creates :class:`~chainer.Variable` objects with ``x_data``\n    and calls ``func`` with the :class:`~chainer.Variable`\\ s to get its\n    result as :class:`~chainer.Variable`.\n    Then, it sets ``y_grad`` array to ``grad`` attribute of the result and\n    calls ``backward`` method to get gradients of the inputs.\n    To check correctness of the gradients, the function calls\n    :func:`numerical_grad` to calculate numerically the gradients and compares\n    the types of gradients with :func:`chainer.testing.assert_allclose`.\n\n    To reduce computational time, it uses a function\n    :math:`g: \\mathbb{R} \\rightarrow \\mathbb{R}^n` defined as\n    :math:`g(\\alpha) = f(\\alpha x)`, where :math:`\\alpha \\in \\mathbb{R}`\n    and :math:`f` is a function which actually\n    you want to test.\n    Its gradient is\n\n    .. math::\n       g'(\\alpha) = f'(\\alpha x) \\cdot x.\n\n    When :math:`\\alpha = 1`, :math:`g'(1) = f'(x) \\cdot x`.\n    So :math:`g'(1)` is calculated with :func:`numerical_grad` and\n    compared with dot product of the gradient :math:`f` and\n    :math:`x`.\n\n    If input objects (``x1_data`` or/and ``x2_data`` in this example) represent\n    integer variables, their gradients are ignored.\n\n    You can simplify a test when ``MyFunc`` gets only one argument::\n\n    >>   check_backward(func, x1_data, gy_data)\n\n    If ``MyFunc`` is a loss function which returns a zero-dimensional\n    array, pass ``None`` to ``gy_data``. In this case, it sets ``1`` to\n    ``grad`` attribute of the result::\n\n    >>   check_backward(my_loss_func, (x1_data, x2_data), None)\n\n    If ``MyFunc`` returns multiple outputs, pass all gradients for outputs\n    as a tuple::\n\n    >>   gy1_data = xp.array(...)\n    >>   gy2_data = xp.array(...)\n    >>   check_backward(func, x1_data, (gy1_data, gy2_data))\n\n    You can also test a :class:`~chainer.Link`.\n    To check gradients of parameters of the link, set a tuple of the parameters\n    to ``params`` arguments::\n\n    >>   check_backward(my_link, (x1_data, x2_data), gy_data,\n    >>                  (my_link.W, my_link.b))\n\n    Note that ``params`` are not ``ndarray``\\ s,\n    but :class:`~chainer.Variables`\\ s.\n\n    Function objects are acceptable as ``func`` argument::\n\n    >>   check_backward(lambda x1, x2: f(x1, x2),\n    >>                  (x1_data, x2_data), gy_data)\n\n    .. note::\n\n       ``func`` is called many times to get numerical gradients for all inputs.\n       This function doesn't work correctly when ``func`` behaves randomly as\n       it gets different gradients.\n\n\n    Args:\n        func (callable): A function which gets :class:`~chainer.Variable`\\ s\n            and returns :class:`~chainer.Variable`\\ s. ``func`` must returns\n            a tuple of :class:`~chainer.Variable`\\ s or one\n            :class:`~chainer.Variable`. You can use :class:`~chainer.Function`\n            object, :class:`~chainer.Link` object or a function satisfying the\n            condition.\n        x_data (ndarray or tuple of ndarrays): A set of ``ndarray``\\ s to be\n            passed to ``func``. If ``x_data`` is one ``ndarray`` object, it is\n            treated as ``(x_data,)``.\n        y_grad (ndarray or tuple of ndarrays or None):\n            A set of ``ndarray``\\ s representing gradients of return-values of\n            ``func``. If ``y_grad`` is one ``ndarray`` object, it is\n            treated as ``(y_grad,)``. If ``func`` is a loss-function,\n            ``y_grad`` should be set to ``None``.\n        params (~chainer.Variable or tuple of ~chainder.Variable):\n            A set of :class:`~chainer.Variable`\\ s whose gradients are\n            checked. When ``func`` is a :class:`~chainer.Link` object,\n            set its parameters as ``params``.\n            If ``params`` is one :class:`~chainer.Variable` object,\n            it is treated as ``(params,)``.\n        eps (float): Epsilon value to be passed to :func:`numerical_grad`.\n        atol (float): Absolute tolerance to be passed to\n            :func:`chainer.testing.assert_allclose`.\n        rtol (float): Relative tolerance to be passed to\n            :func:`chainer.testing.assert_allclose`.\n        no_grads (list of bool): Flag to skip variable for gradient assertion.\n            It should be same length as ``x_data``.\n        dtype (~numpy.dtype): ``x_data``, ``y_grad`` and ``params`` are casted\n            to this dtype when calculating numerical gradients. Only float\n            types and ``None`` are allowed.\n\n    .. seealso::\n       :func:`numerical_grad`\n    "
    if ((dtype is not None) and (numpy.dtype(dtype).kind != 'f')):
        raise ValueError('`dtype` is allowed only float type')
    x_data = _as_tuple(x_data)
    if (y_grad is not None):
        y_grad = _as_tuple(y_grad)
    params = _as_tuple(params)
    xs = [variable.Variable(x) for x in x_data]
    y = func(*xs)
    y = _as_tuple(y)
    y = identity.Identity().apply(y)
    y_grad = _set_y_grad(y, y_grad)
    _clear_grads(xs)
    _clear_grads(params)
    y[0].backward()
    if (dtype is None):
        casted_xs = [variable.Variable(x) for x in x_data]
    else:
        if (numpy.dtype(dtype).kind != 'f'):
            raise ValueError('`dtype` is allowed only float type')
        casted_xs = [variable.Variable((x.astype(dtype, copy=False) if (x.dtype.kind == 'f') else x)) for x in x_data]
        for param in params:
            if (param.data.dtype.kind == 'f'):
                param.data = param.data.astype(dtype, copy=False)
        y_grad = [(g.astype(dtype, copy=False) if ((g is not None) and isinstance(g, (numpy.ndarray, cuda.ndarray)) and (g.dtype.kind == 'f')) else g) for g in y_grad]
    if (no_grads is None):
        no_grads = [(x.dtype.kind != 'f') for x in xs]
    elif (len(no_grads) != len(xs)):
        raise ValueError('Length of no_grads param and xs should be same.\nActual: {0} != {1}'.format(len(no_grads), len(xs)))
    for (skip, x) in six.moves.zip(no_grads, xs):
        if skip:
            assert (x.grad is None)
        elif (x.grad is None):
            raise RuntimeError('gradients of some arguments are not calculated')
    params_grad = [param.grad for param in params]
    param_data = [p.data for p in params]
    casted_data = [x.data.copy() for x in casted_xs]
    xp = cuda.get_array_module(*xs)
    one = xp.array(1.0, dtype)

    def g():
        for (skip, cx, data) in six.moves.zip(no_grads, casted_xs, casted_data):
            if skip:
                continue
            data = (one * data).astype(data.dtype)
            if numpy.isscalar(data):
                data = xp.array(data)
            cx.data = data
        for (param, data) in six.moves.zip(params, param_data):
            if (dtype is not None):
                param_dtype = dtype
            else:
                param_dtype = param.dtype
            param.data = (one * data.astype(param_dtype)).astype(param_dtype)
        _clear_grads(casted_xs)
        _clear_grads(params)
        ys = func(*casted_xs)
        ys = _as_tuple(ys)
        ys_data = tuple((y.data for y in ys))
        for (skip, cx, data) in six.moves.zip(no_grads, casted_xs, casted_data):
            if skip:
                continue
            cx.data = data
        for (param, data) in six.moves.zip(params, param_data):
            param.data = data
        return ys_data
    (gx,) = numerical_grad(g, (one,), y_grad, eps=eps)
    gx_accum = 0
    for (skip, x, cx) in six.moves.zip(no_grads, xs, casted_xs):
        if skip:
            continue
        gxi = x.grad.ravel()
        cxi = cx.data.ravel()
        if (dtype is not None):
            gxi = gxi.astype(dtype, copy=False)
            cxi = cxi.astype(dtype, copy=False)
        gx_accum += gxi.dot(cxi)
    for (p, gpi) in six.moves.zip(params, params_grad):
        gpi = gpi.ravel()
        pi = p.data.ravel()
        if (dtype is not None):
            gpi = gpi.astype(dtype, copy=False)
            pi = pi.astype(dtype, copy=False)
        gx_accum += gpi.dot(pi)
    try:
        testing.assert_allclose(gx, gx_accum, atol=atol, rtol=rtol)
    except AssertionError as e:
        f = six.StringIO()
        f.write('check_backward failed (eps={} atol={} rtol={})\n'.format(eps, atol, rtol))
        for (i, x_) in enumerate(xs):
            f.write('inputs[{}]:\n'.format(i))
            f.write('{}\n'.format(x_))
        for (i, gy_) in enumerate(y_grad):
            f.write('grad_outputs[{}]:\n'.format(i))
            f.write('{}\n'.format(gy_))
        for (i, d_) in enumerate(directions):
            f.write('directions[{}]:\n'.format(i))
            f.write('{}\n'.format(d_))
        f.write('gradients (numeric):  {}\n'.format(gx))
        f.write('gradients (backward): {}\n'.format(gx_accum))
        f.write('\n')
        f.write(str(e))
        raise AssertionError(f.getvalue())