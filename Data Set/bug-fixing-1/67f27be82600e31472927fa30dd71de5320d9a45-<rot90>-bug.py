

def rot90(m, k=1, axes=(0, 1)):
    '\n    Rotate an array by 90 degrees in the plane specified by axes.\n\n    Rotation direction is from the first towards the second axis.\n\n    .. versionadded:: 1.12.0\n\n    Parameters\n    ----------\n    m : array_like\n        Array of two or more dimensions.\n    k : integer\n        Number of times the array is rotated by 90 degrees.\n    axes: (2,) array_like\n        The array is rotated in the plane defined by the axes.\n        Axes must be different.\n\n    Returns\n    -------\n    y : ndarray\n        A rotated view of `m`.\n\n    See Also\n    --------\n    flip : Reverse the order of elements in an array along the given axis.\n    fliplr : Flip an array horizontally.\n    flipud : Flip an array vertically.\n\n    Notes\n    -----\n    rot90(m, k=1, axes=(1,0)) is the reverse of rot90(m, k=1, axes=(0,1))\n    rot90(m, k=1, axes=(1,0)) is equivalent to rot90(m, k=-1, axes=(0,1))\n\n    Examples\n    --------\n    >>> m = np.array([[1,2],[3,4]], int)\n    >>> m\n    array([[1, 2],\n           [3, 4]])\n    >>> np.rot90(m)\n    array([[2, 4],\n           [1, 3]])\n    >>> np.rot90(m, 2)\n    array([[4, 3],\n           [2, 1]])\n    >>> m = np.arange(8).reshape((2,2,2))\n    >>> np.rot90(m, 1, (1,2))\n    array([[[1, 3],\n            [0, 2]],\n\n          [[5, 7],\n           [4, 6]]])\n\n    '
    axes = tuple(axes)
    if (len(axes) != 2):
        raise ValueError('len(axes) must be 2.')
    m = asanyarray(m)
    if ((axes[0] == axes[1]) or (absolute((axes[0] - axes[1])) == m.ndim)):
        raise ValueError('Axes must be different.')
    if ((axes[0] >= m.ndim) or (axes[0] < (- m.ndim)) or (axes[1] >= m.ndim) or (axes[1] < (- m.ndim))):
        raise ValueError('Axes={} out of range for array of ndim={}.'.format(axes, m.ndim))
    k %= 4
    if (k == 0):
        return m[:]
    if (k == 2):
        return flip(flip(m, axes[0]), axes[1])
    axes_list = arange(0, m.ndim)
    (axes_list[axes[0]], axes_list[axes[1]]) = (axes_list[axes[1]], axes_list[axes[0]])
    if (k == 1):
        return transpose(flip(m, axes[1]), axes_list)
    else:
        return flip(transpose(m, axes_list), axes[1])
