def check_backward(func, x_data, y_grad, params=(), eps=0.001, atol=1e-05, rtol=0.0001, no_grads=None, dtype=None, detect_nondifferentiable=False):
    "Test backward procedure of a given function.\n\n    This function automatically checks the backward-process of a given function\n    to ensure that the computed gradients are approximately correct.\n    For example, assuming you've defined a :class:`~chainer.FunctionNode` class\n    ``MyFunc``, that takes two arguments and returns one value, you can wrap\n    it in a ordinary function and check its gradient computations as follows:\n\n    .. code-block:: python\n\n        def func(xs):\n            y, = MyFunc().apply(xs)\n            return y\n\n        x1_data = xp.array(...)\n        x2_data = xp.array(...)\n        gy_data = xp.array(...)\n        check_backward(func, (x1_data, x2_data), gy_data)\n\n    This function creates :class:`~chainer.Variable` objects with ``x_data``\n    and calls ``func`` with the :class:`~chainer.Variable`\\ s to get its\n    result as :class:`~chainer.Variable`.\n    Then, it sets ``y_grad`` array to ``grad`` attribute of the result and\n    calls ``backward`` method to get gradients of the inputs.\n    To check correctness of the gradients, the function calls\n    :func:`numerical_grad` to calculate numerically the gradients and compares\n    the types of gradients with :func:`chainer.testing.assert_allclose`.\n\n    To reduce computational time, it uses directional derivative along a\n    random vector. A function\n    :math:`g: \\mathbb{R} \\rightarrow \\mathbb{R}^n` is defined as\n    :math:`g(\\delta) = f(x + \\delta r)`, where\n    :math:`\\delta \\in \\mathbb{R}`, :math:`r \\in \\mathbb{R}^n`\n    is a random vector\n    and :math:`f` is a function which you want to test.\n    Its gradient is\n\n    .. math::\n       g'(\\delta) = f'(x + \\delta r) \\cdot r.\n\n    Therefore, :math:`g'(0) = f'(x) \\cdot r`.\n    So we can check the correctness of back propagation of :math:`f` indirectly\n    by comparing this equation with the gradient of :math:`g` numerically\n    calculated and that of :math:`f` computed by backprop.\n    If :math:`r` is chosen from uniform distribution, we can conclude with\n    high probability that the gradient of :math:`f` itself is correct.\n\n    If the function is non-differentiable with respect to some input objects,\n    we can check its backprop to such objects by ``no_grads`` argument.\n    ``gradient_check`` computes numerical backward to inputs that correspond to\n    ``False`` in ``no_grads``. It also asserts that the backprop leaves\n    gradients ``None`` for inputs that correspond to ``True`` in ``no_grads``.\n    The default of ``no_grads`` argument is the tuple of truth values whether\n    input objects (``x1_data`` or/and ``x2_data`` in this example) represent\n    integer variables.\n\n    You can simplify a test when ``MyFunc`` gets only one argument:\n\n    .. code-block:: python\n\n        check_backward(func, x1_data, gy_data)\n\n    If ``MyFunc`` is a loss function which returns a zero-dimensional\n    array, pass ``None`` to ``gy_data``. In this case, it sets ``1`` to\n    ``grad`` attribute of the result:\n\n    .. code-block:: python\n\n        check_backward(my_loss_func,\n                       (x1_data, x2_data), None)\n\n    If ``MyFunc`` returns multiple outputs, pass all gradients for outputs\n    as a tuple:\n\n    .. code-block:: python\n\n        gy1_data = xp.array(...)\n        gy2_data = xp.array(...)\n        check_backward(func, x1_data, (gy1_data, gy2_data))\n\n    You can also test a :class:`~chainer.Link`.\n    To check gradients of parameters of the link, set a tuple of the parameters\n    to ``params`` arguments:\n\n    .. code-block:: python\n\n        check_backward(my_link, (x1_data, x2_data), gy_data,\n                       (my_link.W, my_link.b))\n\n    Note that ``params`` are not ``ndarray``\\ s,\n    but :class:`~chainer.Variables`\\ s.\n\n    Function objects are acceptable as ``func`` argument:\n\n    .. code-block:: python\n\n        check_backward(lambda x1, x2: f(x1, x2),\n                       (x1_data, x2_data), gy_data)\n\n    .. note::\n\n       ``func`` is called many times to get numerical gradients for all inputs.\n       This function doesn't work correctly when ``func`` behaves randomly as\n       it gets different gradients.\n\n\n    Args:\n        func (callable): A function which gets :class:`~chainer.Variable`\\ s\n            and returns :class:`~chainer.Variable`\\ s. ``func`` must returns\n            a tuple of :class:`~chainer.Variable`\\ s or one\n            :class:`~chainer.Variable`. You can use a\n            :class:`~chainer.Function`, :class:`~chainer.FunctionNode` or a\n            :class:`~chainer.Link` object or any other function satisfying the\n            condition.\n        x_data (ndarray or tuple of ndarrays): A set of ``ndarray``\\ s to be\n            passed to ``func``. If ``x_data`` is one ``ndarray`` object, it is\n            treated as ``(x_data,)``.\n        y_grad (ndarray or tuple of ndarrays or None):\n            A set of ``ndarray``\\ s representing gradients of return-values of\n            ``func``. If ``y_grad`` is one ``ndarray`` object, it is\n            treated as ``(y_grad,)``. If ``func`` is a loss-function,\n            ``y_grad`` should be set to ``None``.\n        params (~chainer.Variable or tuple of ~chainder.Variable):\n            A set of :class:`~chainer.Variable`\\ s whose gradients are\n            checked. When ``func`` is a :class:`~chainer.Link` object,\n            set its parameters as ``params``.\n            If ``params`` is one :class:`~chainer.Variable` object,\n            it is treated as ``(params,)``.\n        eps (float): Epsilon value to be passed to :func:`numerical_grad`.\n        atol (float): Absolute tolerance to be passed to\n            :func:`chainer.testing.assert_allclose`.\n        rtol (float): Relative tolerance to be passed to\n            :func:`chainer.testing.assert_allclose`.\n        no_grads (list of bool): Flag to skip variable for gradient assertion.\n            It should be same length as ``x_data``.\n        dtype (~numpy.dtype): ``x_data``, ``y_grad`` and ``params`` are casted\n            to this dtype when calculating numerical gradients. Only float\n            types and ``None`` are allowed.\n        detect_nondifferentiable (bool):\n            If ``True``, check for non-differentiable inputs is enabled.\n            If ``func`` is non-differentiable at ``x_data``, ``check_backward``\n            raises :class:`~chainer.gradient_check.NondifferentiableError`.\n\n    .. seealso::\n       :func:`numerical_grad`\n    "
    _CheckBackward(func, x_data, y_grad, params, eps, atol, rtol, no_grads, dtype, detect_nondifferentiable).run()