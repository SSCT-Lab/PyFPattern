def parse_auth_header(header):
    if isinstance(header, bytes):
        header = header.decode('latin1')
    try:
        return dict(map(_make_key_value, header.split(' ', 1)[1].split(',')))
    except Exception:
        return {
            
        }