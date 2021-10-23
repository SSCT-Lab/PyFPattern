

def _read_array_header(fp, version):
    '\n    see read_array_header_1_0\n    '
    import struct
    if (version == (1, 0)):
        hlength_type = '<H'
    elif (version == (2, 0)):
        hlength_type = '<I'
    else:
        raise ValueError('Invalid version {!r}'.format(version))
    hlength_str = _read_bytes(fp, struct.calcsize(hlength_type), 'array header length')
    header_length = struct.unpack(hlength_type, hlength_str)[0]
    header = _read_bytes(fp, header_length, 'array header')
    header = _filter_header(header)
    try:
        d = safe_eval(header)
    except SyntaxError as e:
        msg = 'Cannot parse header: {!r}\nException: {!r}'
        raise ValueError(msg.format(header, e))
    if (not isinstance(d, dict)):
        msg = 'Header is not a dictionary: {!r}'
        raise ValueError(msg.format(d))
    keys = sorted(d.keys())
    if (keys != ['descr', 'fortran_order', 'shape']):
        msg = 'Header does not contain the correct keys: {!r}'
        raise ValueError(msg.format(keys))
    if ((not isinstance(d['shape'], tuple)) or (not numpy.all([isinstance(x, (int, long)) for x in d['shape']]))):
        msg = 'shape is not valid: {!r}'
        raise ValueError(msg.format(d['shape']))
    if (not isinstance(d['fortran_order'], bool)):
        msg = 'fortran_order is not a valid bool: {!r}'
        raise ValueError(msg.format(d['fortran_order']))
    try:
        dtype = descr_to_dtype(d['descr'])
    except TypeError as e:
        msg = 'descr is not a valid dtype descriptor: {!r}'
        raise ValueError(msg.format(d['descr']))
    return (d['shape'], d['fortran_order'], dtype)
