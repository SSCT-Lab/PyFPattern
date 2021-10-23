@array_function_dispatch(_multidot_dispatcher)
def multi_dot(arrays):
    '\n    Compute the dot product of two or more arrays in a single function call,\n    while automatically selecting the fastest evaluation order.\n\n    `multi_dot` chains `numpy.dot` and uses optimal parenthesization\n    of the matrices [1]_ [2]_. Depending on the shapes of the matrices,\n    this can speed up the multiplication a lot.\n\n    If the first argument is 1-D it is treated as a row vector.\n    If the last argument is 1-D it is treated as a column vector.\n    The other arguments must be 2-D.\n\n    Think of `multi_dot` as::\n\n        def multi_dot(arrays): return functools.reduce(np.dot, arrays)\n\n\n    Parameters\n    ----------\n    arrays : sequence of array_like\n        If the first argument is 1-D it is treated as row vector.\n        If the last argument is 1-D it is treated as column vector.\n        The other arguments must be 2-D.\n\n    Returns\n    -------\n    output : ndarray\n        Returns the dot product of the supplied arrays.\n\n    See Also\n    --------\n    dot : dot multiplication with two arguments.\n\n    References\n    ----------\n\n    .. [1] Cormen, "Introduction to Algorithms", Chapter 15.2, p. 370-378\n    .. [2] https://en.wikipedia.org/wiki/Matrix_chain_multiplication\n\n    Examples\n    --------\n    `multi_dot` allows you to write::\n\n    >>> from numpy.linalg import multi_dot\n    >>> # Prepare some data\n    >>> A = np.random.random((10000, 100))\n    >>> B = np.random.random((100, 1000))\n    >>> C = np.random.random((1000, 5))\n    >>> D = np.random.random((5, 333))\n    >>> # the actual dot multiplication\n    >>> _ = multi_dot([A, B, C, D])\n\n    instead of::\n\n    >>> _ = np.dot(np.dot(np.dot(A, B), C), D)\n    >>> # or\n    >>> _ = A.dot(B).dot(C).dot(D)\n\n    Notes\n    -----\n    The cost for a matrix multiplication can be calculated with the\n    following function::\n\n        def cost(A, B):\n            return A.shape[0] * A.shape[1] * B.shape[1]\n\n    Assume we have three matrices\n    :math:`A_{10x100}, B_{100x5}, C_{5x50}`.\n\n    The costs for the two different parenthesizations are as follows::\n\n        cost((AB)C) = 10*100*5 + 10*5*50   = 5000 + 2500   = 7500\n        cost(A(BC)) = 10*100*50 + 100*5*50 = 50000 + 25000 = 75000\n\n    '
    n = len(arrays)
    if (n < 2):
        raise ValueError('Expecting at least two arrays.')
    elif (n == 2):
        return dot(arrays[0], arrays[1])
    arrays = [asanyarray(a) for a in arrays]
    (ndim_first, ndim_last) = (arrays[0].ndim, arrays[(- 1)].ndim)
    if (arrays[0].ndim == 1):
        arrays[0] = atleast_2d(arrays[0])
    if (arrays[(- 1)].ndim == 1):
        arrays[(- 1)] = atleast_2d(arrays[(- 1)]).T
    _assert_2d(*arrays)
    if (n == 3):
        result = _multi_dot_three(arrays[0], arrays[1], arrays[2])
    else:
        order = _multi_dot_matrix_chain_order(arrays)
        result = _multi_dot(arrays, order, 0, (n - 1))
    if ((ndim_first == 1) and (ndim_last == 1)):
        return result[(0, 0)]
    elif ((ndim_first == 1) or (ndim_last == 1)):
        return result.ravel()
    else:
        return result