

@array_function_dispatch(_intersect1d_dispatcher)
def intersect1d(ar1, ar2, assume_unique=False, return_indices=False):
    '\n    Find the intersection of two arrays.\n\n    Return the sorted, unique values that are in both of the input arrays.\n\n    Parameters\n    ----------\n    ar1, ar2 : array_like\n        Input arrays. Will be flattened if not already 1D.\n    assume_unique : bool\n        If True, the input arrays are both assumed to be unique, which\n        can speed up the calculation.  Default is False.\n    return_indices : bool\n        If True, the indices which correspond to the intersection of the two\n        arrays are returned. The first instance of a value is used if there are\n        multiple. Default is False.\n\n        .. versionadded:: 1.15.0\n\n    Returns\n    -------\n    intersect1d : ndarray\n        Sorted 1D array of common and unique elements.\n    comm1 : ndarray\n        The indices of the first occurrences of the common values in `ar1`.\n        Only provided if `return_indices` is True.\n    comm2 : ndarray\n        The indices of the first occurrences of the common values in `ar2`.\n        Only provided if `return_indices` is True.\n\n\n    See Also\n    --------\n    numpy.lib.arraysetops : Module with a number of other functions for\n                            performing set operations on arrays.\n\n    Examples\n    --------\n    >>> np.intersect1d([1, 3, 4, 3], [3, 1, 2, 1])\n    array([1, 3])\n\n    To intersect more than two arrays, use functools.reduce:\n\n    >>> from functools import reduce\n    >>> reduce(np.intersect1d, ([1, 3, 4, 3], [3, 1, 2, 1], [6, 3, 4, 2]))\n    array([3])\n\n    To return the indices of the values common to the input arrays\n    along with the intersected values:\n    >>> x = np.array([1, 1, 2, 3, 4])\n    >>> y = np.array([2, 1, 4, 6])\n    >>> xy, x_ind, y_ind = np.intersect1d(x, y, return_indices=True)\n    >>> x_ind, y_ind\n    (array([0, 2, 4]), array([1, 0, 2]))\n    >>> xy, x[x_ind], y[y_ind]\n    (array([1, 2, 4]), array([1, 2, 4]), array([1, 2, 4]))\n\n    '
    ar1 = np.asanyarray(ar1)
    ar2 = np.asanyarray(ar2)
    if (not assume_unique):
        if return_indices:
            (ar1, ind1) = unique(ar1, return_index=True)
            (ar2, ind2) = unique(ar2, return_index=True)
        else:
            ar1 = unique(ar1)
            ar2 = unique(ar2)
    else:
        ar1 = ar1.ravel()
        ar2 = ar2.ravel()
    aux = np.concatenate((ar1, ar2))
    if return_indices:
        aux_sort_indices = np.argsort(aux, kind='mergesort')
        aux = aux[aux_sort_indices]
    else:
        aux.sort()
    mask = (aux[1:] == aux[:(- 1)])
    int1d = aux[:(- 1)][mask]
    if return_indices:
        ar1_indices = aux_sort_indices[:(- 1)][mask]
        ar2_indices = (aux_sort_indices[1:][mask] - ar1.size)
        if (not assume_unique):
            ar1_indices = ind1[ar1_indices]
            ar2_indices = ind2[ar2_indices]
        return (int1d, ar1_indices, ar2_indices)
    else:
        return int1d
