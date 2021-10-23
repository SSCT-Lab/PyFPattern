def flip(m, axis):
    '\n    Reverse the order of elements in an array along the given axis.\n\n    The shape of the array is preserved, but the elements are reordered.\n\n    .. versionadded:: 1.12.0\n\n    Parameters\n    ----------\n    m : array_like\n        Input array.\n    axis : integer\n        Axis in array, which entries are reversed.\n\n\n    Returns\n    -------\n    out : array_like\n        A view of `m` with the entries of axis reversed.  Since a view is\n        returned, this operation is done in constant time.\n\n    See Also\n    --------\n    flipud : Flip an array vertically (axis=0).\n    fliplr : Flip an array horizontally (axis=1).\n\n    Notes\n    -----\n    flip(m, 0) is equivalent to flipud(m).\n    flip(m, 1) is equivalent to fliplr(m).\n    flip(m, n) corresponds to ``m[...,::-1,...]`` with ``::-1`` at position n.\n\n    Examples\n    --------\n    >>> A = np.arange(8).reshape((2,2,2))\n    >>> A\n    array([[[0, 1],\n            [2, 3]],\n\n           [[4, 5],\n            [6, 7]]])\n\n    >>> flip(A, 0)\n    array([[[4, 5],\n            [6, 7]],\n\n           [[0, 1],\n            [2, 3]]])\n\n    >>> flip(A, 1)\n    array([[[2, 3],\n            [0, 1]],\n\n           [[6, 7],\n            [4, 5]]])\n\n    >>> A = np.random.randn(3,4,5)\n    >>> np.all(flip(A,2) == A[:,:,::-1,...])\n    True\n    '
    if (not hasattr(m, 'ndim')):
        m = asarray(m)
    indexer = ([slice(None)] * m.ndim)
    try:
        indexer[axis] = slice(None, None, (- 1))
    except IndexError:
        raise ValueError(('axis=%i is invalid for the %i-dimensional input array' % (axis, m.ndim)))
    return m[tuple(indexer)]