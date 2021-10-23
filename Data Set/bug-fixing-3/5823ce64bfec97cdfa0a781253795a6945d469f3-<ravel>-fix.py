@set_module('mxnet.symbol.numpy')
def ravel(x, order='C'):
    '\n    ravel(x)\n\n    Return a contiguous flattened array.\n    A 1-D array, containing the elements of the input, is returned.  A copy is\n    made only if needed.\n\n    Parameters\n    ----------\n    x : _Symbol\n        Input array.  The elements in `x` are read in row-major, C-style order and\n        packed as a 1-D array.\n    order : `C`, optional\n        Only support row-major, C-style order.\n\n    Returns\n    -------\n    y : _Symbol\n        y is an array of the same subtype as `x`, with shape ``(x.size,)``.\n        Note that matrices are special cased for backward compatibility, if `x`\n        is a matrix, then y is a 1-D ndarray.\n\n    Notes\n    -----\n    This function differs from the original numpy.arange in the following aspects:\n        - Only support row-major, C-style order.\n    '
    if (order != 'C'):
        raise NotImplementedError('order {} is not supported'.format(order))
    if isinstance(x, numeric_types):
        return _np.reshape(x, (- 1))
    elif isinstance(x, _Symbol):
        return _npi.reshape(x, (- 1))
    else:
        raise TypeError('type {} not supported'.format(str(type(x))))