def _prepend_med(arr, pad_amt, num, axis=(- 1)):
    '\n    Prepend `pad_amt` median values along `axis`.\n\n    Parameters\n    ----------\n    arr : ndarray\n        Input array of arbitrary shape.\n    pad_amt : int\n        Amount of padding to prepend.\n    num : int\n        Depth into `arr` along `axis` to calculate median.\n        Range: [1, `arr.shape[axis]`] or None (entire axis)\n    axis : int\n        Axis along which to pad `arr`.\n\n    Returns\n    -------\n    padarr : ndarray\n        Output array, with `pad_amt` values prepended along `axis`. The\n        prepended region is the median of the first `num` values along `axis`.\n\n    '
    if (pad_amt == 0):
        return arr
    if (num == 1):
        return _prepend_edge(arr, pad_amt, axis)
    if (num is not None):
        if (num >= arr.shape[axis]):
            num = None
    med_slice = _slice_first(arr.shape, num, axis=axis)
    med_chunk = np.median(arr[med_slice], axis=axis, keepdims=True)
    _round_ifneeded(med_chunk, arr.dtype)
    return np.concatenate((med_chunk.repeat(pad_amt, axis).astype(arr.dtype), arr), axis=axis)