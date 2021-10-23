def pandas_dtype(dtype):
    '\n    Converts input into a pandas only dtype object or a numpy dtype object.\n\n    Parameters\n    ----------\n    dtype : object to be converted\n\n    Returns\n    -------\n    np.dtype or a pandas dtype\n\n    Raises\n    ------\n    TypeError if not a dtype\n\n    '
    if isinstance(dtype, np.ndarray):
        return dtype.dtype
    elif isinstance(dtype, np.dtype):
        return dtype
    result = (_pandas_registry.find(dtype) or registry.find(dtype))
    if (result is not None):
        return result
    elif isinstance(dtype, (PandasExtensionDtype, ExtensionDtype)):
        return dtype
    try:
        npdtype = np.dtype(dtype)
    except Exception:
        if (not isinstance(dtype, string_types)):
            raise TypeError('data type not understood')
        raise TypeError("data type '{}' not understood".format(dtype))
    if (is_hashable(dtype) and (dtype in [object, np.object_, 'object', 'O'])):
        return npdtype
    elif (npdtype.kind == 'O'):
        raise TypeError("dtype '{}' not understood".format(dtype))
    return npdtype