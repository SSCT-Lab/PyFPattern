def _append_ramp(arr, pad_amt, end, axis=(- 1)):
    '\n    Append linear ramp along `axis`.\n\n    Parameters\n    ----------\n    arr : ndarray\n        Input array of arbitrary shape.\n    pad_amt : int\n        Amount of padding to append.\n    end : scalar\n        Constal value to use. For best results should be of type `arr.dtype`;\n        if not `arr.dtype` will be cast to `arr.dtype`.\n    axis : int\n        Axis along which to pad `arr`.\n\n    Returns\n    -------\n    padarr : ndarray\n        Output array, with `pad_amt` values appended along `axis`. The\n        appended region ramps linearly from the edge value to `end`.\n\n    '
    if (pad_amt == 0):
        return arr
    padshape = tuple(((x if (i != axis) else pad_amt) for (i, x) in enumerate(arr.shape)))
    ramp_arr = _arange_ndarray(arr, padshape, axis, reverse=False).astype(np.float64)
    edge_slice = tuple(((slice(None) if (i != axis) else slice((x - 1), x)) for (i, x) in enumerate(arr.shape)))
    edge_pad = arr[edge_slice].repeat(pad_amt, axis)
    slope = ((end - edge_pad) / float(pad_amt))
    ramp_arr = (ramp_arr * slope)
    ramp_arr += edge_pad
    _round_ifneeded(ramp_arr, arr.dtype)
    return np.concatenate((arr, ramp_arr.astype(arr.dtype)), axis=axis)