def _prepend_max(arr, pad_amt, num, axis=(- 1)):
    '\n    Prepend `pad_amt` maximum values along `axis`.\n\n    Parameters\n    ----------\n    arr : ndarray\n        Input array of arbitrary shape.\n    pad_amt : int\n        Amount of padding to prepend.\n    num : int\n        Depth into `arr` along `axis` to calculate maximum.\n        Range: [1, `arr.shape[axis]`] or None (entire axis)\n    axis : int\n        Axis along which to pad `arr`.\n\n    Returns\n    -------\n    padarr : ndarray\n        Output array, with `pad_amt` values appended along `axis`. The\n        prepended region is the maximum of the first `num` values along\n        `axis`.\n\n    '
    if (pad_amt == 0):
        return arr
    if (num == 1):
        return _prepend_edge(arr, pad_amt, axis)
    if (num is not None):
        if (num >= arr.shape[axis]):
            num = None
    max_slice = _slice_first(arr.shape, num, axis=axis)
    max_chunk = arr[max_slice].max(axis=axis, keepdims=True)
    return np.concatenate((max_chunk.repeat(pad_amt, axis=axis), arr), axis=axis)