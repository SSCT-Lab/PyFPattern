

def as_variable(obj):
    'Converts an array or a variable into :class:`~chainer.Variable`.\n\n    This is a convenient function to get a :class:`~chainer.Variable` object\n    transparently from a raw array or a variable.\n\n    Note that this function should only be used for type consistency (i.e., to\n    enforce the return value of an API having type :class:`~chainer.Varialbe`).\n    The :class:`~chainer.Variable.requires_grad` flag is kept as is; if ``obj``\n    is a raw array, the newly created variable has ``requires_grad = False``.\n    In order to make a variable w.r.t. which you want to compute the gradient,\n    you should use :class:`~chainer.Variable` directly.\n\n    Args:\n        obj (numpy.ndarray or cupy.ndarray or ~chainer.Variable): An array or\n            a variable that you want to convert to :class:`~chainer.Variable`.\n\n    Returns:\n        ~chainer.Variable:\n        A variable converted from ``obj``. If ``obj`` is a raw array, this is a\n        new :class:`~chainer.Variable` object that wraps the array. If ``obj``\n        is already a :class:`~chainer.Variable` object, this function returns\n        ``obj`` as is.\n\n    '
    if isinstance(obj, Variable):
        return obj
    return Variable(obj, requires_grad=False)
