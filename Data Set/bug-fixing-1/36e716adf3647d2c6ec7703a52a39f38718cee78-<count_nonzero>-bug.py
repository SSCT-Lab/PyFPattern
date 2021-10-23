

def count_nonzero(a, axis=None):
    '\n    Counts the number of non-zero values in the array ``a``.\n\n    The word "non-zero" is in reference to the Python 2.x\n    built-in method ``__nonzero__()`` (renamed ``__bool__()``\n    in Python 3.x) of Python objects that tests an object\'s\n    "truthfulness". For example, any number is considered\n    truthful if it is nonzero, whereas any string is considered\n    truthful if it is not the empty string. Thus, this function\n    (recursively) counts how many elements in ``a`` (and in\n    sub-arrays thereof) have their ``__nonzero__()`` or ``__bool__()``\n    method evaluated to ``True``.\n\n    Parameters\n    ----------\n    a : array_like\n        The array for which to count non-zeros.\n    axis : int or tuple, optional\n        Axis or tuple of axes along which to count non-zeros.\n        Default is None, meaning that non-zeros will be counted\n        along a flattened version of ``a``.\n\n        .. versionadded:: 1.12.0\n\n    Returns\n    -------\n    count : int or array of int\n        Number of non-zero values in the array along a given axis.\n        Otherwise, the total number of non-zero values in the array\n        is returned.\n\n    See Also\n    --------\n    nonzero : Return the coordinates of all the non-zero values.\n\n    Examples\n    --------\n    >>> np.count_nonzero(np.eye(4))\n    4\n    >>> np.count_nonzero([[0,1,7,0,0],[3,0,0,2,19]])\n    5\n    >>> np.count_nonzero([[0,1,7,0,0],[3,0,0,2,19]], axis=0)\n    array([1, 1, 1, 1, 1])\n    >>> np.count_nonzero([[0,1,7,0,0],[3,0,0,2,19]], axis=1)\n    array([2, 3])\n\n    '
    if ((axis is None) or (isinstance(axis, tuple) and (axis == ()))):
        return multiarray.count_nonzero(a)
    a = asanyarray(a)
    if (a.dtype == bool):
        return a.sum(axis=axis, dtype=np.intp)
    if issubdtype(a.dtype, np.number):
        return (a != 0).sum(axis=axis, dtype=np.intp)
    if issubdtype(a.dtype, np.character):
        nullstr = a.dtype.type('')
        return (a != nullstr).sum(axis=axis, dtype=np.intp)
    axis = asarray(normalize_axis_tuple(axis, a.ndim))
    counts = np.apply_along_axis(multiarray.count_nonzero, axis[0], a)
    if (axis.size == 1):
        return counts.astype(np.intp, copy=False)
    else:
        return counts.sum(axis=tuple((axis[1:] - (axis[1:] > axis[0]))), dtype=np.intp)
