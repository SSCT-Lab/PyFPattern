def _append_min(arr, pad_amt, num, axis=(- 1)):
    '\n    Append `pad_amt` median values along `axis`.\n\n    Parameters\n    ----------\n    arr : ndarray\n        Input array of arbitrary shape.\n    pad_amt : int\n        Amount of padding to append.\n    num : int\n        Depth into `arr` along `axis` to calculate minimum.\n        Range: [1, `arr.shape[axis]`] or None (entire axis)\n    axis : int\n        Axis along which to pad `arr`.\n\n    Returns\n    -------\n    padarr : ndarray\n        Output array, with `pad_amt` values appended along `axis`. The\n        appended region is the minimum of the final `num` values along `axis`.\n\n    '
    if (pad_amt == 0):
        return arr
    if (num == 1):
        return _append_edge(arr, pad_amt, axis)
    if (num is not None):
        if (num >= arr.shape[axis]):
            num = None
    end = (arr.shape[axis] - 1)
    if (num is not None):
        min_slice = tuple(((slice(None) if (i != axis) else slice(end, (end - num), (- 1))) for (i, x) in enumerate(arr.shape)))
    else:
        min_slice = tuple((slice(None) for x in arr.shape))
    pad_singleton = tuple(((x if (i != axis) else 1) for (i, x) in enumerate(arr.shape)))
    min_chunk = arr[min_slice].min(axis=axis).reshape(pad_singleton)
    return np.concatenate((arr, min_chunk.repeat(pad_amt, axis=axis)), axis=axis)