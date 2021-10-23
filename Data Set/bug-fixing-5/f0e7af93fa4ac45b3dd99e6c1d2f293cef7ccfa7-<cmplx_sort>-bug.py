def cmplx_sort(p):
    'Sort roots based on magnitude.\n\n    Parameters\n    ----------\n    p : array_like\n        The roots to sort, as a 1-D array.\n\n    Returns\n    -------\n    p_sorted : ndarray\n        Sorted roots.\n    indx : ndarray\n        Array of indices needed to sort the input `p`.\n\n    Examples\n    --------\n    >>> from scipy import signal\n    >>> vals = [1, 4, 1+1.j, 3]\n    >>> p_sorted, indx = signal.cmplx_sort(vals)\n    >>> p_sorted\n    array([1.+0.j, 1.+1.j, 3.+0.j, 4.+0.j])\n    >>> indx\n    array([0, 2, 3, 1])\n    '
    p = asarray(p)
    indx = argsort(abs(p))
    return (take(p, indx, 0), indx)