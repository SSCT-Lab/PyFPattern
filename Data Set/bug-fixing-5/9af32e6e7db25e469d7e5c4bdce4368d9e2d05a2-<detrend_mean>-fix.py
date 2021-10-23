def detrend_mean(x, axis=None):
    '\n    Return x minus the mean(x).\n\n    Parameters\n    ----------\n    x : array or sequence\n        Array or sequence containing the data\n        Can have any dimensionality\n\n    axis : integer\n        The axis along which to take the mean.  See numpy.mean for a\n        description of this argument.\n\n    See Also\n    --------\n    :func:`demean`\n        This function is the same as :func:`demean` except for the default\n        *axis*.\n\n    :func:`detrend_linear`\n\n    :func:`detrend_none`\n        :func:`detrend_linear` and :func:`detrend_none` are other detrend\n        algorithms.\n\n    :func:`detrend`\n        :func:`detrend` is a wrapper around all the detrend algorithms.\n    '
    x = np.asarray(x)
    if ((axis is not None) and ((axis + 1) > x.ndim)):
        raise ValueError(('axis(=%s) out of bounds' % axis))
    return (x - x.mean(axis, keepdims=True))