def _construction_repr(dtype, include_align=False, short=False):
    "\n    Creates a string repr of the dtype, excluding the 'dtype()' part\n    surrounding the object. This object may be a string, a list, or\n    a dict depending on the nature of the dtype. This\n    is the object passed as the first parameter to the dtype\n    constructor, and if no additional constructor parameters are\n    given, will reproduce the exact memory layout.\n\n    Parameters\n    ----------\n    short : bool\n        If true, this creates a shorter repr using 'kind' and 'itemsize', instead\n        of the longer type name.\n\n    include_align : bool\n        If true, this includes the 'align=True' parameter\n        inside the struct dtype construction dict when needed. Use this flag\n        if you want a proper repr string without the 'dtype()' part around it.\n\n        If false, this does not preserve the\n        'align=True' parameter or sticky NPY_ALIGNED_STRUCT flag for\n        struct arrays like the regular repr does, because the 'align'\n        flag is not part of first dtype constructor parameter. This\n        mode is intended for a full 'repr', where the 'align=True' is\n        provided as the second parameter.\n    "
    if (dtype.fields is not None):
        return _struct_str(dtype, include_align=include_align)
    elif dtype.subdtype:
        return _subarray_str(dtype)
    byteorder = _byte_order_str(dtype)
    if (dtype.type == np.bool_):
        if short:
            return "'?'"
        else:
            return "'bool'"
    elif (dtype.type == np.object_):
        return "'O'"
    elif (dtype.type == np.string_):
        if _isunsized(dtype):
            return "'S'"
        else:
            return ("'S%d'" % dtype.itemsize)
    elif (dtype.type == np.unicode_):
        if _isunsized(dtype):
            return ("'%sU'" % byteorder)
        else:
            return ("'%sU%d'" % (byteorder, (dtype.itemsize / 4)))
    elif (dtype.type == np.void):
        if _isunsized(dtype):
            return "'V'"
        else:
            return ("'V%d'" % dtype.itemsize)
    elif (dtype.type == np.datetime64):
        return ("'%sM8%s'" % (byteorder, _datetime_metadata_str(dtype)))
    elif (dtype.type == np.timedelta64):
        return ("'%sm8%s'" % (byteorder, _datetime_metadata_str(dtype)))
    elif np.issubdtype(dtype, np.number):
        if (short or (dtype.byteorder not in ('=', '|'))):
            return ("'%s%c%d'" % (byteorder, dtype.kind, dtype.itemsize))
        else:
            kindstrs = {
                'u': 'uint',
                'i': 'int',
                'f': 'float',
                'c': 'complex',
            }
            try:
                kindstr = kindstrs[dtype.kind]
            except KeyError:
                raise RuntimeError('internal dtype repr error, unknown kind {!r}'.format(dtype.kind))
            return ("'%s%d'" % (kindstr, (8 * dtype.itemsize)))
    elif (dtype.isbuiltin == 2):
        return dtype.type.__name__
    else:
        raise RuntimeError('Internal error: NumPy dtype unrecognized type number')