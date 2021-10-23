def dtype_from_ctypes_type(t):
    '\n    Construct a dtype object from a ctypes type\n    '
    if issubclass(t, _ctypes.Array):
        return _from_ctypes_array(t)
    elif issubclass(t, _ctypes._Pointer):
        raise TypeError('ctypes pointers have no dtype equivalent')
    elif issubclass(t, _ctypes.Structure):
        return _from_ctypes_structure(t)
    elif issubclass(t, _ctypes.Union):
        return dtype_from_ctypes_union(t)
    elif isinstance(t._type_, str):
        return dtype_from_ctypes_scalar(t)
    else:
        raise NotImplementedError('Unknown ctypes type {}'.format(t.__name__))