def _prepend_edge(arr, pad_amt, axis=(- 1)):
    '\n    Prepend `pad_amt` to `arr` along `axis` by extending edge values.\n\n    Parameters\n    ----------\n    arr : ndarray\n        Input array of arbitrary shape.\n    pad_amt : int\n        Amount of padding to prepend.\n    axis : int\n        Axis along which to pad `arr`.\n\n    Returns\n    -------\n    padarr : ndarray\n        Output array, extended by `pad_amt` edge values appended along `axis`.\n\n    '
    if (pad_amt == 0):
        return arr
    edge_slice = _slice_first(arr.shape, 1, axis=axis)
    edge_arr = arr[edge_slice]
    return _do_prepend(arr, edge_arr.repeat(pad_amt, axis=axis), axis)