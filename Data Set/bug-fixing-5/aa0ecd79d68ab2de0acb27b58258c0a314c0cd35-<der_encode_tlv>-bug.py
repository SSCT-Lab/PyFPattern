def der_encode_tlv(tag, value):
    return ((force_bytes(chr(tag)) + der_encode_length(len(value))) + value)