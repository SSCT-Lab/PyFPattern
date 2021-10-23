def get_random_string(length=12, allowed_chars='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'):
    '\n    Return a securely generated random string.\n\n    The default length of 12 with the a-z, A-Z, 0-9 character set returns\n    a 71-bit value. log_2((26+26+10)^12) =~ 71 bits\n    '
    return ''.join((secrets.choice(allowed_chars) for i in range(length)))