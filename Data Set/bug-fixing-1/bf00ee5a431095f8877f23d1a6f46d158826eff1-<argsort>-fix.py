

@array_function_dispatch(_argsort_dispatcher)
def argsort(a, axis=(- 1), kind='quicksort', order=None):
    "\n    Returns the indices that would sort an array.\n\n    Perform an indirect sort along the given axis using the algorithm specified\n    by the `kind` keyword. It returns an array of indices of the same shape as\n    `a` that index data along the given axis in sorted order.\n\n    Parameters\n    ----------\n    a : array_like\n        Array to sort.\n    axis : int or None, optional\n        Axis along which to sort.  The default is -1 (the last axis). If None,\n        the flattened array is used.\n    kind : {'quicksort', 'mergesort', 'heapsort', 'timsort', 'stable'}, optional\n        Sorting algorithm.\n    order : str or list of str, optional\n        When `a` is an array with fields defined, this argument specifies\n        which fields to compare first, second, etc.  A single field can\n        be specified as a string, and not all fields need be specified,\n        but unspecified fields will still be used, in the order in which\n        they come up in the dtype, to break ties.\n\n    Returns\n    -------\n    index_array : ndarray, int\n        Array of indices that sort `a` along the specified `axis`.\n        If `a` is one-dimensional, ``a[index_array]`` yields a sorted `a`.\n        More generally, ``np.take_along_axis(a, index_array, axis=axis)``\n        always yields the sorted `a`, irrespective of dimensionality.\n\n    See Also\n    --------\n    sort : Describes sorting algorithms used.\n    lexsort : Indirect stable sort with multiple keys.\n    ndarray.sort : Inplace sort.\n    argpartition : Indirect partial sort.\n\n    Notes\n    -----\n    See `sort` for notes on the different sorting algorithms.\n\n    As of NumPy 1.4.0 `argsort` works with real/complex arrays containing\n    nan values. The enhanced sort order is documented in `sort`.\n\n    Examples\n    --------\n    One dimensional array:\n\n    >>> x = np.array([3, 1, 2])\n    >>> np.argsort(x)\n    array([1, 2, 0])\n\n    Two-dimensional array:\n\n    >>> x = np.array([[0, 3], [2, 2]])\n    >>> x\n    array([[0, 3],\n           [2, 2]])\n\n    >>> ind = np.argsort(x, axis=0)  # sorts along first axis (down)\n    >>> ind\n    array([[0, 1],\n           [1, 0]])\n    >>> np.take_along_axis(x, ind, axis=0)  # same as np.sort(x, axis=0)\n    array([[0, 2],\n           [2, 3]])\n\n    >>> ind = np.argsort(x, axis=1)  # sorts along last axis (across)\n    >>> ind\n    array([[0, 1],\n           [0, 1]])\n    >>> np.take_along_axis(x, ind, axis=1)  # same as np.sort(x, axis=1)\n    array([[0, 3],\n           [2, 2]])\n\n    Indices of the sorted elements of a N-dimensional array:\n\n    >>> ind = np.unravel_index(np.argsort(x, axis=None), x.shape)\n    >>> ind\n    (array([0, 1, 1, 0]), array([0, 0, 1, 1]))\n    >>> x[ind]  # same as np.sort(x, axis=None)\n    array([0, 2, 2, 3])\n\n    Sorting with keys:\n\n    >>> x = np.array([(1, 0), (0, 1)], dtype=[('x', '<i4'), ('y', '<i4')])\n    >>> x\n    array([(1, 0), (0, 1)],\n          dtype=[('x', '<i4'), ('y', '<i4')])\n\n    >>> np.argsort(x, order=('x','y'))\n    array([1, 0])\n\n    >>> np.argsort(x, order=('y','x'))\n    array([0, 1])\n\n    "
    return _wrapfunc(a, 'argsort', axis=axis, kind=kind, order=order)
