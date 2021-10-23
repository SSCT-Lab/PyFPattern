@array_function_dispatch(_sort_dispatcher)
def sort(a, axis=(- 1), kind=None, order=None):
    "\n    Return a sorted copy of an array.\n\n    Parameters\n    ----------\n    a : array_like\n        Array to be sorted.\n    axis : int or None, optional\n        Axis along which to sort. If None, the array is flattened before\n        sorting. The default is -1, which sorts along the last axis.\n    kind : {'quicksort', 'mergesort', 'heapsort', 'stable'}, optional\n        Sorting algorithm. The default is 'quicksort'. Note that both 'stable'\n        and 'mergesort' use timsort or radix sort under the covers and, in general,\n        the actual implementation will vary with data type. The 'mergesort' option\n        is retained for backwards compatibility.\n\n        .. versionchanged:: 1.15.0.\n           The 'stable' option was added.\n\n    order : str or list of str, optional\n        When `a` is an array with fields defined, this argument specifies\n        which fields to compare first, second, etc.  A single field can\n        be specified as a string, and not all fields need be specified,\n        but unspecified fields will still be used, in the order in which\n        they come up in the dtype, to break ties.\n\n    Returns\n    -------\n    sorted_array : ndarray\n        Array of the same type and shape as `a`.\n\n    See Also\n    --------\n    ndarray.sort : Method to sort an array in-place.\n    argsort : Indirect sort.\n    lexsort : Indirect stable sort on multiple keys.\n    searchsorted : Find elements in a sorted array.\n    partition : Partial sort.\n\n    Notes\n    -----\n    The various sorting algorithms are characterized by their average speed,\n    worst case performance, work space size, and whether they are stable. A\n    stable sort keeps items with the same key in the same relative\n    order. The four algorithms implemented in NumPy have the following\n    properties:\n\n    =========== ======= ============= ============ ========\n       kind      speed   worst case    work space   stable\n    =========== ======= ============= ============ ========\n    'quicksort'    1     O(n^2)            0          no\n    'heapsort'     3     O(n*log(n))       0          no\n    'mergesort'    2     O(n*log(n))      ~n/2        yes\n    'timsort'      2     O(n*log(n))      ~n/2        yes\n    =========== ======= ============= ============ ========\n\n    .. note:: The datatype determines which of 'mergesort' or 'timsort'\n       is actually used, even if 'mergesort' is specified. User selection\n       at a finer scale is not currently available.\n\n    All the sort algorithms make temporary copies of the data when\n    sorting along any but the last axis.  Consequently, sorting along\n    the last axis is faster and uses less space than sorting along\n    any other axis.\n\n    The sort order for complex numbers is lexicographic. If both the real\n    and imaginary parts are non-nan then the order is determined by the\n    real parts except when they are equal, in which case the order is\n    determined by the imaginary parts.\n\n    Previous to numpy 1.4.0 sorting real and complex arrays containing nan\n    values led to undefined behaviour. In numpy versions >= 1.4.0 nan\n    values are sorted to the end. The extended sort order is:\n\n      * Real: [R, nan]\n      * Complex: [R + Rj, R + nanj, nan + Rj, nan + nanj]\n\n    where R is a non-nan real value. Complex values with the same nan\n    placements are sorted according to the non-nan part if it exists.\n    Non-nan values are sorted as before.\n\n    .. versionadded:: 1.12.0\n\n    quicksort has been changed to `introsort <https://en.wikipedia.org/wiki/Introsort>`_.\n    When sorting does not make enough progress it switches to\n    `heapsort <https://en.wikipedia.org/wiki/Heapsort>`_.\n    This implementation makes quicksort O(n*log(n)) in the worst case.\n\n    'stable' automatically chooses the best stable sorting algorithm\n    for the data type being sorted.\n    It, along with 'mergesort' is currently mapped to\n    `timsort <https://en.wikipedia.org/wiki/Timsort>`_\n    or `radix sort <https://en.wikipedia.org/wiki/Radix_sort>`_\n    depending on the data type.\n    API forward compatibility currently limits the\n    ability to select the implementation and it is hardwired for the different\n    data types.\n\n    .. versionadded:: 1.17.0\n\n    Timsort is added for better performance on already or nearly\n    sorted data. On random data timsort is almost identical to\n    mergesort. It is now used for stable sort while quicksort is still the\n    default sort if none is chosen. For timsort details, refer to\n    `CPython listsort.txt <https://github.com/python/cpython/blob/3.7/Objects/listsort.txt>`_.\n    'mergesort' and 'stable' are mapped to radix sort for integer data types. Radix sort is an\n    O(n) sort instead of O(n log n).\n\n    Examples\n    --------\n    >>> a = np.array([[1,4],[3,1]])\n    >>> np.sort(a)                # sort along the last axis\n    array([[1, 4],\n           [1, 3]])\n    >>> np.sort(a, axis=None)     # sort the flattened array\n    array([1, 1, 3, 4])\n    >>> np.sort(a, axis=0)        # sort along the first axis\n    array([[1, 1],\n           [3, 4]])\n\n    Use the `order` keyword to specify a field to use when sorting a\n    structured array:\n\n    >>> dtype = [('name', 'S10'), ('height', float), ('age', int)]\n    >>> values = [('Arthur', 1.8, 41), ('Lancelot', 1.9, 38),\n    ...           ('Galahad', 1.7, 38)]\n    >>> a = np.array(values, dtype=dtype)       # create a structured array\n    >>> np.sort(a, order='height')                        # doctest: +SKIP\n    array([('Galahad', 1.7, 38), ('Arthur', 1.8, 41),\n           ('Lancelot', 1.8999999999999999, 38)],\n          dtype=[('name', '|S10'), ('height', '<f8'), ('age', '<i4')])\n\n    Sort by age, then height if ages are equal:\n\n    >>> np.sort(a, order=['age', 'height'])               # doctest: +SKIP\n    array([('Galahad', 1.7, 38), ('Lancelot', 1.8999999999999999, 38),\n           ('Arthur', 1.8, 41)],\n          dtype=[('name', '|S10'), ('height', '<f8'), ('age', '<i4')])\n\n    "
    if (axis is None):
        a = asanyarray(a).flatten()
        axis = (- 1)
    else:
        a = asanyarray(a).copy(order='K')
    a.sort(axis=axis, kind=kind, order=order)
    return a