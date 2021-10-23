

def broadcast_arrays(*args, **kwargs):
    '\n    Broadcast any number of arrays against each other.\n\n    Parameters\n    ----------\n    `*args` : array_likes\n        The arrays to broadcast.\n\n    subok : bool, optional\n        If True, then sub-classes will be passed-through, otherwise\n        the returned arrays will be forced to be a base-class array (default).\n\n    Returns\n    -------\n    broadcasted : list of arrays\n        These arrays are views on the original arrays.  They are typically\n        not contiguous.  Furthermore, more than one element of a\n        broadcasted array may refer to a single memory location.  If you\n        need to write to the arrays, make copies first.\n\n    Examples\n    --------\n    >>> x = np.array([[1,2,3]])\n    >>> y = np.array([[1],[2],[3]])\n    >>> np.broadcast_arrays(x, y)\n    [array([[1, 2, 3],\n           [1, 2, 3],\n           [1, 2, 3]]), array([[1, 1, 1],\n           [2, 2, 2],\n           [3, 3, 3]])]\n\n    Here is a useful idiom for getting contiguous copies instead of\n    non-contiguous views.\n\n    >>> [np.array(a) for a in np.broadcast_arrays(x, y)]\n    [array([[1, 2, 3],\n           [1, 2, 3],\n           [1, 2, 3]]), array([[1, 1, 1],\n           [2, 2, 2],\n           [3, 3, 3]])]\n\n    '
    subok = kwargs.pop('subok', False)
    if kwargs:
        raise TypeError('broadcast_arrays() got an unexpected keyword argument {}'.format(kwargs.pop()))
    args = [np.array(_m, copy=False, subok=subok) for _m in args]
    shape = _broadcast_shape(*args)
    if all(((array.shape == shape) for array in args)):
        return args
    return [_broadcast_to(array, shape, subok=subok, readonly=False) for array in args]
