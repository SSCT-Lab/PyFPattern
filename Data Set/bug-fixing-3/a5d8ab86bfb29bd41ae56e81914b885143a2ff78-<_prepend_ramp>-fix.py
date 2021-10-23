def _prepend_ramp(arr, pad_amt, end, axis=(- 1)):
    '\n    Prepend linear ramp along `axis`.\n\n    Parameters\n    ----------\n    arr : ndarray\n        Input array of arbitrary shape.\n    pad_amt : int\n        Amount of padding to prepend.\n    end : scalar\n        Constal value to use. For best results should be of type `arr.dtype`;\n        if not `arr.dtype` will be cast to `arr.dtype`.\n    axis : int\n        Axis along which to pad `arr`.\n\n    Returns\n    -------\n    padarr : ndarray\n        Output array, with `pad_amt` values prepended along `axis`. The\n        prepended region ramps linearly from the edge value to `end`.\n\n    '
    if (pad_amt == 0):
        return arr
    padshape = tuple(((x if (i != axis) else pad_amt) for (i, x) in enumerate(arr.shape)))
    ramp_arr = _arange_ndarray(arr, padshape, axis, reverse=True).astype(np.float64)
    edge_slice = _slice_first(arr.shape, 1, axis=axis)
    edge_pad = arr[edge_slice].repeat(pad_amt, axis)
    slope = ((end - edge_pad) / float(pad_amt))
    ramp_arr = (ramp_arr * slope)
    ramp_arr += edge_pad
    _round_ifneeded(ramp_arr, arr.dtype)
    return _do_prepend(arr, ramp_arr, axis)