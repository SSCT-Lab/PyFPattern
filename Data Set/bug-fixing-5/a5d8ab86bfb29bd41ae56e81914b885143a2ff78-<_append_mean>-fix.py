def _append_mean(arr, pad_amt, num, axis=(- 1)):
    '\n    Append `pad_amt` mean values along `axis`.\n\n    Parameters\n    ----------\n    arr : ndarray\n        Input array of arbitrary shape.\n    pad_amt : int\n        Amount of padding to append.\n    num : int\n        Depth into `arr` along `axis` to calculate mean.\n        Range: [1, `arr.shape[axis]`] or None (entire axis)\n    axis : int\n        Axis along which to pad `arr`.\n\n    Returns\n    -------\n    padarr : ndarray\n        Output array, with `pad_amt` values appended along `axis`. The\n        appended region is the maximum of the final `num` values along `axis`.\n\n    '
    if (pad_amt == 0):
        return arr
    if (num == 1):
        return _append_edge(arr, pad_amt, axis)
    if (num is not None):
        if (num >= arr.shape[axis]):
            num = None
    if (num is not None):
        mean_slice = _slice_last(arr.shape, num, axis=axis)
    else:
        mean_slice = tuple((slice(None) for x in arr.shape))
    mean_chunk = arr[mean_slice].mean(axis=axis, keepdims=True)
    _round_ifneeded(mean_chunk, arr.dtype)
    return _do_append(arr, mean_chunk.repeat(pad_amt, axis), axis=axis)