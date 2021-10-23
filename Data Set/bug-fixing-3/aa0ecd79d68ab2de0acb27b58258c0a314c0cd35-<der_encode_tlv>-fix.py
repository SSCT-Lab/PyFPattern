def der_encode_tlv(tag, value):
    return ((struct.pack('!B', tag) + der_encode_length(len(value))) + value)