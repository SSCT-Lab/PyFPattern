

def mean(x, axis=None, keepdims=False):
    'Mean of a tensor, alongside the specified axis.\n    '
    dtype = None
    if (('int' in x.dtype) or (x.dtype == 'bool')):
        dtype = _FLOATX
    return T.mean(x, axis=axis, keepdims=keepdims, dtype=dtype)
