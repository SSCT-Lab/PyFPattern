def __repr__(dtype):
    if (dtype.fields is not None):
        return _struct_repr(dtype)
    else:
        return 'dtype({})'.format(_construction_repr(dtype, include_align=True))