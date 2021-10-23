def der_encode_integer_value(val):
    if (not isinstance(val, six.integer_types)):
        raise TypeError('int')
    if (val == 0):
        return b'\x00'
    sign = 0
    out = b''
    while (val != sign):
        byte = (val & 255)
        out = (force_bytes(chr(byte)) + out)
        sign = ((- 1) if ((byte & 128) == 128) else 0)
        val >>= 8
    return out