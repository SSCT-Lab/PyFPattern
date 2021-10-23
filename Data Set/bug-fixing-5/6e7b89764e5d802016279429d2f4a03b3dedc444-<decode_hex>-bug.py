def decode_hex(hexstring):
    if (len(hexstring) < 3):
        return hexstring
    if (hexstring[:2] == '0x'):
        return hexstring[2:].decode('hex')
    else:
        return hexstring