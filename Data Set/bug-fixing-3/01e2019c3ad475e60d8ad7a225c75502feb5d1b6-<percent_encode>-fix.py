def percent_encode(val):
    if isinstance(val, six.text_type):
        val = val.encode('utf8', errors='replace')
    return quote(val).replace('%7E', '~').replace('/', '%2F')