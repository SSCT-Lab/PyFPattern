def select(condlist, choicelist, default=0):
    '\n    Return an array drawn from elements in choicelist, depending on conditions.\n\n    Parameters\n    ----------\n    condlist : list of bool ndarrays\n        The list of conditions which determine from which array in `choicelist`\n        the output elements are taken. When multiple conditions are satisfied,\n        the first one encountered in `condlist` is used.\n    choicelist : list of ndarrays\n        The list of arrays from which the output elements are taken. It has\n        to be of the same length as `condlist`.\n    default : scalar, optional\n        The element inserted in `output` when all conditions evaluate to False.\n\n    Returns\n    -------\n    output : ndarray\n        The output at position m is the m-th element of the array in\n        `choicelist` where the m-th element of the corresponding array in\n        `condlist` is True.\n\n    See Also\n    --------\n    where : Return elements from one of two arrays depending on condition.\n    take, choose, compress, diag, diagonal\n\n    Examples\n    --------\n    >>> x = np.arange(10)\n    >>> condlist = [x<3, x>5]\n    >>> choicelist = [x, x**2]\n    >>> np.select(condlist, choicelist)\n    array([ 0,  1,  2,  0,  0,  0, 36, 49, 64, 81])\n\n    '
    if (len(condlist) != len(choicelist)):
        raise ValueError('list of cases must be same length as list of conditions')
    if (len(condlist) == 0):
        warnings.warn('select with an empty condition list is not possibleand will be deprecated', DeprecationWarning, stacklevel=2)
        return np.asarray(default)[()]
    choicelist = [np.asarray(choice) for choice in choicelist]
    choicelist.append(np.asarray(default))
    dtype = np.result_type(*choicelist)
    condlist = np.broadcast_arrays(*condlist)
    choicelist = np.broadcast_arrays(*choicelist)
    deprecated_ints = False
    for i in range(len(condlist)):
        cond = condlist[i]
        if (cond.dtype.type is not np.bool_):
            if np.issubdtype(cond.dtype, np.integer):
                condlist[i] = condlist[i].astype(bool)
                deprecated_ints = True
            else:
                raise ValueError('invalid entry {} in condlist: should be boolean ndarray'.format(i))
    if deprecated_ints:
        msg = 'select condlists containing integer ndarrays is deprecated and will be removed in the future. Use `.astype(bool)` to convert to bools.'
        warnings.warn(msg, DeprecationWarning, stacklevel=2)
    if (choicelist[0].ndim == 0):
        result_shape = condlist[0].shape
    else:
        result_shape = np.broadcast_arrays(condlist[0], choicelist[0])[0].shape
    result = np.full(result_shape, choicelist[(- 1)], dtype)
    choicelist = choicelist[(- 2)::(- 1)]
    condlist = condlist[::(- 1)]
    for (choice, cond) in zip(choicelist, condlist):
        np.copyto(result, choice, where=cond)
    return result