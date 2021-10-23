def der_encode_length(length):
    if (length <= 127):
        return force_bytes(chr(length))
    out = b''
    while (length > 0):
        out = (force_bytes(chr((length & 255))) + out)
        length >>= 8
    out = (force_bytes(chr((len(out) | 128))) + out)
    return out