def _numeric_arrays(arrays, kinds='buifc'):
    '\n    See if a list of arrays are all numeric.\n\n    Parameters\n    ----------\n    ndarrays : array or list of arrays\n        arrays to check if numeric.\n    numeric_kinds : string-like\n        The dtypes of the arrays to be checked. If the dtype.kind of\n        the ndarrays are not in this string the function returns False and\n        otherwise returns True.\n    '
    if (type(arrays) == ndarray):
        return (arrays.dtype.kind in kinds)
    for array_ in arrays:
        if (array_.dtype.kind not in kinds):
            return False
    return True