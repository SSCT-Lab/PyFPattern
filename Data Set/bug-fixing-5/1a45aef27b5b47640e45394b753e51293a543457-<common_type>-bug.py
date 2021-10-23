def common_type(*arrays):
    "\n    Return a scalar type which is common to the input arrays.\n\n    The return type will always be an inexact (i.e. floating point) scalar\n    type, even if all the arrays are integer arrays. If one of the inputs is\n    an integer array, the minimum precision type that is returned is a\n    64-bit floating point dtype.\n\n    All input arrays can be safely cast to the returned dtype without loss\n    of information.\n\n    Parameters\n    ----------\n    array1, array2, ... : ndarrays\n        Input arrays.\n\n    Returns\n    -------\n    out : data type code\n        Data type code.\n\n    See Also\n    --------\n    dtype, mintypecode\n\n    Examples\n    --------\n    >>> np.common_type(np.arange(2, dtype=np.float32))\n    <type 'numpy.float32'>\n    >>> np.common_type(np.arange(2, dtype=np.float32), np.arange(2))\n    <type 'numpy.float64'>\n    >>> np.common_type(np.arange(4), np.array([45, 6.j]), np.array([45.0]))\n    <type 'numpy.complex128'>\n\n    "
    is_complex = False
    precision = 0
    for a in arrays:
        t = a.dtype.type
        if iscomplexobj(a):
            is_complex = True
        if issubclass(t, _nx.integer):
            p = 2
        else:
            p = array_precision.get(t, None)
            if (p is None):
                raise TypeError("can't get common type for non-numeric array")
        precision = max(precision, p)
    if is_complex:
        return array_type[1][precision]
    else:
        return array_type[0][precision]