def percent_encode(val):
    return quote(val.encode('utf8', errors='replace')).replace('%7E', '~').replace('/', '%2F')