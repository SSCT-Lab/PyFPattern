def _append_edge(arr, pad_amt, axis=(- 1)):
    '\n    Append `pad_amt` to `arr` along `axis` by extending edge values.\n\n    Parameters\n    ----------\n    arr : ndarray\n        Input array of arbitrary shape.\n    pad_amt : int\n        Amount of padding to append.\n    axis : int\n        Axis along which to pad `arr`.\n\n    Returns\n    -------\n    padarr : ndarray\n        Output array, extended by `pad_amt` edge values prepended along\n        `axis`.\n\n    '
    if (pad_amt == 0):
        return arr
    edge_slice = _slice_last(arr.shape, 1, axis=axis)
    edge_arr = arr[edge_slice]
    return _do_append(arr, edge_arr.repeat(pad_amt, axis=axis), axis)