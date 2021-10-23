def decode_hex(hexstring):
    if (len(hexstring) < 3):
        return hexstring
    if (hexstring[:2] == '0x'):
        return to_text(binascii.unhexlify(hexstring[2:]))
    else:
        return hexstring