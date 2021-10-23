@array_function_dispatch(_matrix_power_dispatcher)
def matrix_power(a, n):
    '\n    Raise a square matrix to the (integer) power `n`.\n\n    For positive integers `n`, the power is computed by repeated matrix\n    squarings and matrix multiplications. If ``n == 0``, the identity matrix\n    of the same shape as M is returned. If ``n < 0``, the inverse\n    is computed and then raised to the ``abs(n)``.\n\n    .. note:: Stacks of object matrices are not currently supported.\n\n    Parameters\n    ----------\n    a : (..., M, M) array_like\n        Matrix to be "powered".\n    n : int\n        The exponent can be any integer or long integer, positive,\n        negative, or zero.\n\n    Returns\n    -------\n    a**n : (..., M, M) ndarray or matrix object\n        The return value is the same shape and type as `M`;\n        if the exponent is positive or zero then the type of the\n        elements is the same as those of `M`. If the exponent is\n        negative the elements are floating-point.\n\n    Raises\n    ------\n    LinAlgError\n        For matrices that are not square or that (for negative powers) cannot\n        be inverted numerically.\n\n    Examples\n    --------\n    >>> from numpy.linalg import matrix_power\n    >>> i = np.array([[0, 1], [-1, 0]]) # matrix equiv. of the imaginary unit\n    >>> matrix_power(i, 3) # should = -i\n    array([[ 0, -1],\n           [ 1,  0]])\n    >>> matrix_power(i, 0)\n    array([[1, 0],\n           [0, 1]])\n    >>> matrix_power(i, -3) # should = 1/(-i) = i, but w/ f.p. elements\n    array([[ 0.,  1.],\n           [-1.,  0.]])\n\n    Somewhat more sophisticated example\n\n    >>> q = np.zeros((4, 4))\n    >>> q[0:2, 0:2] = -i\n    >>> q[2:4, 2:4] = i\n    >>> q # one of the three quaternion units not equal to 1\n    array([[ 0., -1.,  0.,  0.],\n           [ 1.,  0.,  0.,  0.],\n           [ 0.,  0.,  0.,  1.],\n           [ 0.,  0., -1.,  0.]])\n    >>> matrix_power(q, 2) # = -np.eye(4)\n    array([[-1.,  0.,  0.,  0.],\n           [ 0., -1.,  0.,  0.],\n           [ 0.,  0., -1.,  0.],\n           [ 0.,  0.,  0., -1.]])\n\n    '
    a = asanyarray(a)
    _assertRankAtLeast2(a)
    _assertNdSquareness(a)
    try:
        n = operator.index(n)
    except TypeError:
        raise TypeError('exponent must be an integer')
    if (a.dtype != object):
        fmatmul = matmul
    elif (a.ndim == 2):
        fmatmul = dot
    else:
        raise NotImplementedError('matrix_power not supported for stacks of object arrays')
    if (n == 0):
        a = empty_like(a)
        a[...] = eye(a.shape[(- 2)], dtype=a.dtype)
        return a
    elif (n < 0):
        a = inv(a)
        n = abs(n)
    if (n == 1):
        return a
    elif (n == 2):
        return fmatmul(a, a)
    elif (n == 3):
        return fmatmul(fmatmul(a, a), a)
    z = result = None
    while (n > 0):
        z = (a if (z is None) else fmatmul(z, z))
        (n, bit) = divmod(n, 2)
        if bit:
            result = (z if (result is None) else fmatmul(result, z))
    return result