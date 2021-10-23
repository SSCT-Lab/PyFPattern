def _ureduce(a, func, **kwargs):
    "\n    Internal Function.\n    Call `func` with `a` as first argument swapping the axes to use extended\n    axis on functions that don't support it natively.\n\n    Returns result and a.shape with axis dims set to 1.\n\n    Parameters\n    ----------\n    a : array_like\n        Input array or object that can be converted to an array.\n    func : callable\n        Reduction function capable of receiving a single axis argument.\n        It is is called with `a` as first argument followed by `kwargs`.\n    kwargs : keyword arguments\n        additional keyword arguments to pass to `func`.\n\n    Returns\n    -------\n    result : tuple\n        Result of func(a, **kwargs) and a.shape with axis dims set to 1\n        which can be used to reshape the result to the same shape a ufunc with\n        keepdims=True would produce.\n\n    "
    a = np.asanyarray(a)
    axis = kwargs.get('axis', None)
    if (axis is not None):
        keepdim = list(a.shape)
        nd = a.ndim
        axis = _nx.normalize_axis_tuple(axis, nd)
        for ax in axis:
            keepdim[ax] = 1
        if (len(axis) == 1):
            kwargs['axis'] = axis[0]
        else:
            keep = (set(range(nd)) - set(axis))
            nkeep = len(keep)
            for (i, s) in enumerate(sorted(keep)):
                a = a.swapaxes(i, s)
            a = a.reshape((a.shape[:nkeep] + ((- 1),)))
            kwargs['axis'] = (- 1)
        keepdim = tuple(keepdim)
    else:
        keepdim = ((1,) * a.ndim)
    r = func(a, **kwargs)
    return (r, keepdim)