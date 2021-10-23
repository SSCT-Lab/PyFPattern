def _prepend_const(arr, pad_amt, val, axis=(- 1)):
    '\n    Prepend constant `val` along `axis` of `arr`.\n\n    Parameters\n    ----------\n    arr : ndarray\n        Input array of arbitrary shape.\n    pad_amt : int\n        Amount of padding to prepend.\n    val : scalar\n        Constant value to use. For best results should be of type `arr.dtype`;\n        if not `arr.dtype` will be cast to `arr.dtype`.\n    axis : int\n        Axis along which to pad `arr`.\n\n    Returns\n    -------\n    padarr : ndarray\n        Output array, with `pad_amt` constant `val` prepended along `axis`.\n\n    '
    if (pad_amt == 0):
        return arr
    padshape = tuple(((x if (i != axis) else pad_amt) for (i, x) in enumerate(arr.shape)))
    return np.concatenate((np.full(padshape, val, dtype=arr.dtype), arr), axis=axis)