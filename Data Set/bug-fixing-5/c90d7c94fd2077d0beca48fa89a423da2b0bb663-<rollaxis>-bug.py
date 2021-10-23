def rollaxis(a, axis, start=0):
    '\n    Roll the specified axis backwards, until it lies in a given position.\n\n    Parameters\n    ----------\n    a : ndarray\n        Input array.\n    axis : int\n        The axis to roll backwards.  The positions of the other axes do not\n        change relative to one another.\n    start : int, optional\n        The axis is rolled until it lies before this position.  The default,\n        0, results in a "complete" roll.\n\n    Returns\n    -------\n    res : ndarray\n        For NumPy >= 1.10.0 a view of `a` is always returned. For earlier\n        NumPy versions a view of `a` is returned only if the order of the\n        axes is changed, otherwise the input array is returned.\n\n    See Also\n    --------\n    moveaxis : Move array axes to new positions.\n    roll : Roll the elements of an array by a number of positions along a\n        given axis.\n\n    Examples\n    --------\n    >>> a = np.ones((3,4,5,6))\n    >>> np.rollaxis(a, 3, 1).shape\n    (3, 6, 4, 5)\n    >>> np.rollaxis(a, 2).shape\n    (5, 3, 4, 6)\n    >>> np.rollaxis(a, 1, 4).shape\n    (3, 5, 6, 4)\n\n    '
    n = a.ndim
    if (axis < 0):
        axis += n
    if (start < 0):
        start += n
    msg = 'rollaxis: %s (%d) must be >=0 and < %d'
    if (not (0 <= axis < n)):
        raise ValueError((msg % ('axis', axis, n)))
    if (not (0 <= start < (n + 1))):
        raise ValueError((msg % ('start', start, (n + 1))))
    if (axis < start):
        start -= 1
    if (axis == start):
        return a[...]
    axes = list(range(0, n))
    axes.remove(axis)
    axes.insert(start, axis)
    return a.transpose(axes)