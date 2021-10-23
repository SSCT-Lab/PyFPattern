

def unique(ar, return_index=False, return_inverse=False, return_counts=False, axis=None):
    "\n    Find the unique elements of an array.\n\n    Returns the sorted unique elements of an array. There are three optional\n    outputs in addition to the unique elements: the indices of the input array\n    that give the unique values, the indices of the unique array that\n    reconstruct the input array, and the number of times each unique value\n    comes up in the input array.\n\n    Parameters\n    ----------\n    ar : array_like\n        Input array. Unless `axis` is specified, this will be flattened if it\n        is not already 1-D.\n    return_index : bool, optional\n        If True, also return the indices of `ar` (along the specified axis,\n        if provided, or in the flattened array) that result in the unique array.\n    return_inverse : bool, optional\n        If True, also return the indices of the unique array (for the specified\n        axis, if provided) that can be used to reconstruct `ar`.\n    return_counts : bool, optional\n        If True, also return the number of times each unique item appears\n        in `ar`.\n\n        .. versionadded:: 1.9.0\n\n    axis : int or None, optional\n        The axis to operate on. If None, `ar` will be flattened beforehand.\n        Otherwise, duplicate items will be removed along the provided axis,\n        with all the other axes belonging to the each of the unique elements.\n        Object arrays or structured arrays that contain objects are not\n        supported if the `axis` kwarg is used.\n\n        .. versionadded:: 1.13.0\n\n\n\n    Returns\n    -------\n    unique : ndarray\n        The sorted unique values.\n    unique_indices : ndarray, optional\n        The indices of the first occurrences of the unique values in the\n        original array. Only provided if `return_index` is True.\n    unique_inverse : ndarray, optional\n        The indices to reconstruct the original array from the\n        unique array. Only provided if `return_inverse` is True.\n    unique_counts : ndarray, optional\n        The number of times each of the unique values comes up in the\n        original array. Only provided if `return_counts` is True.\n\n        .. versionadded:: 1.9.0\n\n    See Also\n    --------\n    numpy.lib.arraysetops : Module with a number of other functions for\n                            performing set operations on arrays.\n\n    Examples\n    --------\n    >>> np.unique([1, 1, 2, 2, 3, 3])\n    array([1, 2, 3])\n    >>> a = np.array([[1, 1], [2, 3]])\n    >>> np.unique(a)\n    array([1, 2, 3])\n\n    Return the unique rows of a 2D array\n\n    >>> a = np.array([[1, 0, 0], [1, 0, 0], [2, 3, 4]])\n    >>> np.unique(a, axis=0)\n    array([[1, 0, 0], [2, 3, 4]])\n\n    Return the indices of the original array that give the unique values:\n\n    >>> a = np.array(['a', 'b', 'b', 'c', 'a'])\n    >>> u, indices = np.unique(a, return_index=True)\n    >>> u\n    array(['a', 'b', 'c'],\n           dtype='|S1')\n    >>> indices\n    array([0, 1, 3])\n    >>> a[indices]\n    array(['a', 'b', 'c'],\n           dtype='|S1')\n\n    Reconstruct the input array from the unique values:\n\n    >>> a = np.array([1, 2, 6, 4, 2, 3, 2])\n    >>> u, indices = np.unique(a, return_inverse=True)\n    >>> u\n    array([1, 2, 3, 4, 6])\n    >>> indices\n    array([0, 1, 4, 3, 1, 2, 1])\n    >>> u[indices]\n    array([1, 2, 6, 4, 2, 3, 2])\n\n    "
    ar = np.asanyarray(ar)
    if (axis is None):
        return _unique1d(ar, return_index, return_inverse, return_counts)
    if (not ((- ar.ndim) <= axis < ar.ndim)):
        raise ValueError('Invalid axis kwarg specified for unique')
    ar = np.swapaxes(ar, axis, 0)
    (orig_shape, orig_dtype) = (ar.shape, ar.dtype)
    ar = ar.reshape(orig_shape[0], (- 1))
    ar = np.ascontiguousarray(ar)
    if (ar.dtype.char in ((np.typecodes['AllInteger'] + np.typecodes['Datetime']) + 'S')):
        dtype = np.dtype((np.void, (ar.dtype.itemsize * ar.shape[1])))
    else:
        dtype = [('f{i}'.format(i=i), ar.dtype) for i in range(ar.shape[1])]
    try:
        consolidated = ar.view(dtype)
    except TypeError:
        msg = 'The axis argument to unique is not supported for dtype {dt}'
        raise TypeError(msg.format(dt=ar.dtype))

    def reshape_uniq(uniq):
        uniq = uniq.view(orig_dtype)
        uniq = uniq.reshape((- 1), *orig_shape[1:])
        uniq = np.swapaxes(uniq, 0, axis)
        return uniq
    output = _unique1d(consolidated, return_index, return_inverse, return_counts)
    if (not (return_index or return_inverse or return_counts)):
        return reshape_uniq(output)
    else:
        uniq = reshape_uniq(output[0])
        return ((uniq,) + output[1:])
