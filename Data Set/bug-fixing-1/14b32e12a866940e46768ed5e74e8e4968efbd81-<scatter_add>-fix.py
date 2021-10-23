

def scatter_add(a, slices, value):
    "Adds given values to specified elements of an array.\n\n    It adds ``value`` to the specified elements of ``a``.\n    If all of the indices target different locations, the operation of\n    :func:`scatter_add` is equivalent to ``a[slices] = a[slices] + value``.\n    If there are multiple elements targeting the same location,\n    :func:`scatter_add` uses all of these values for addition. On the other\n    hand, ``a[slices] = a[slices] + value`` only adds the contribution from one\n    of the indices targeting the same location.\n\n    Note that just like an array indexing, negative indices are interpreted as\n    counting from the end of an array.\n\n    Example\n    -------\n    >>> import numpy\n    >>> import cupy\n    >>> a = cupy.zeros((6,), dtype=numpy.float32)\n    >>> i = cupy.array([1, 0, 1])\n    >>> v = cupy.array([1., 1., 1.])\n    >>> cupy.scatter_add(a, i, v);\n    >>> a\n    array([ 1.,  2.,  0.,  0.,  0.,  0.], dtype=float32)\n\n    Args:\n        a (ndarray): An array that gets added.\n        slices: It is integer, slices, ellipsis, numpy.newaxis,\n            integer array-like or tuple of them.\n            It works for slices used for\n            :func:`cupy.ndarray.__getitem__` and\n            :func:`cupy.ndarray.__setitem__`.\n        v (array-like): Values to increment ``a`` at referenced locations.\n\n    .. note::\n        It only supports types that are supported by CUDA's atomicAdd.\n        The supported types are ``numpy.float32``, ``numpy.int32``,\n        ``numpy.uint32``, ``numpy.uint64`` and ``numpy.ulonglong``.\n\n    .. note::\n        :func:`scatter_add` does not raise an error when indices exceed size of\n        axes. Instead, it wraps indices.\n\n    "
    a.scatter_add(slices, value)
