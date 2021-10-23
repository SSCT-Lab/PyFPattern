def _append_edge(arr, pad_amt, axis=(- 1)):
    '\n    Append `pad_amt` to `arr` along `axis` by extending edge values.\n\n    Parameters\n    ----------\n    arr : ndarray\n        Input array of arbitrary shape.\n    pad_amt : int\n        Amount of padding to append.\n    axis : int\n        Axis along which to pad `arr`.\n\n    Returns\n    -------\n    padarr : ndarray\n        Output array, extended by `pad_amt` edge values prepended along\n        `axis`.\n\n    '
    if (pad_amt == 0):
        return arr
    edge_slice = tuple(((slice(None) if (i != axis) else (arr.shape[axis] - 1)) for (i, x) in enumerate(arr.shape)))
    pad_singleton = tuple(((x if (i != axis) else 1) for (i, x) in enumerate(arr.shape)))
    edge_arr = arr[edge_slice].reshape(pad_singleton)
    return np.concatenate((arr, edge_arr.repeat(pad_amt, axis=axis)), axis=axis)