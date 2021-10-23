def normalize_axis_tuple(axis, ndim, argname=None, allow_duplicate=False):
    '\n    Normalizes an axis argument into a tuple of non-negative integer axes.\n\n    This handles shorthands such as ``1`` and converts them to ``(1,)``,\n    as well as performing the handling of negative indices covered by\n    `normalize_axis_index`.\n\n    By default, this forbids axes from being specified multiple times.\n\n    Used internally by multi-axis-checking logic.\n\n    .. versionadded:: 1.13.0\n\n    Parameters\n    ----------\n    axis : int, iterable of int\n        The un-normalized index or indices of the axis.\n    ndim : int\n        The number of dimensions of the array that `axis` should be normalized\n        against.\n    argname : str, optional\n        A prefix to put before the error message, typically the name of the\n        argument.\n    allow_duplicate : bool, optional\n        If False, the default, disallow an axis from being specified twice.\n\n    Returns\n    -------\n    normalized_axes : tuple of int\n        The normalized axis index, such that `0 <= normalized_axis < ndim`\n\n    Raises\n    ------\n    AxisError\n        If any axis provided is out of range\n    ValueError\n        If an axis is repeated\n\n    See also\n    --------\n    normalize_axis_index : normalizing a single scalar axis\n    '
    try:
        axis = [operator.index(axis)]
    except TypeError:
        axis = tuple(axis)
    axis = tuple((normalize_axis_index(ax, ndim, argname) for ax in axis))
    if ((not allow_duplicate) and (len(set(axis)) != len(axis))):
        if argname:
            raise ValueError('repeated axis in `{}` argument'.format(argname))
        else:
            raise ValueError('repeated axis')
    return axis