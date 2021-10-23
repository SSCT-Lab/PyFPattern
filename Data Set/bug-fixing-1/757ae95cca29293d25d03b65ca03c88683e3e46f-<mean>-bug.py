

def mean(x, axis=None, keepdims=False):
    dtype = None
    if ('int' in x.dtype):
        dtype = _FLOATX
    return T.mean(x, axis=axis, keepdims=keepdims, dtype=dtype)
