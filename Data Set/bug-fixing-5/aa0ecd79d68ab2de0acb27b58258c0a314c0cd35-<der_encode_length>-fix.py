def der_encode_length(length):
    if (length <= 127):
        return struct.pack('!B', length)
    out = b''
    while (length > 0):
        out = (struct.pack('!B', (length & 255)) + out)
        length >>= 8
    out = (struct.pack('!B', (len(out) | 128)) + out)
    return out