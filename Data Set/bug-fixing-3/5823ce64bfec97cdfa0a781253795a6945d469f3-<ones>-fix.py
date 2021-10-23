@set_module('mxnet.symbol.numpy')
def ones(shape, dtype=_np.float32, order='C', ctx=None):
    "Return a new array of given shape and type, filled with ones.\n    This function currently only supports storing multi-dimensional data\n    in row-major (C-style).\n\n    Parameters\n    ----------\n    shape : int or tuple of int\n        The shape of the empty array.\n    dtype : str or numpy.dtype, optional\n        An optional value type. Default is `numpy.float32`. Note that this\n        behavior is different from NumPy's `ones` function where `float64`\n        is the default value, because `float32` is considered as the default\n        data type in deep learning.\n    order : {'C'}, optional, default: 'C'\n        How to store multi-dimensional data in memory, currently only row-major\n        (C-style) is supported.\n    ctx : Context, optional\n        An optional device context (default is the current default context).\n\n    Returns\n    -------\n    out : _Symbol\n        Array of ones with the given shape, dtype, and ctx.\n    "
    if (order != 'C'):
        raise NotImplementedError
    if (ctx is None):
        ctx = current_context()
    dtype = (_np.float32 if (dtype is None) else dtype)
    return _npi.ones(shape=shape, ctx=ctx, dtype=dtype)