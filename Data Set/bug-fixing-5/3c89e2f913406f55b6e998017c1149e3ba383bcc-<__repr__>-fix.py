def __repr__(dtype):
    arg_str = _construction_repr(dtype, include_align=False)
    if dtype.isalignedstruct:
        arg_str = (arg_str + ', align=True')
    return 'dtype({})'.format(arg_str)