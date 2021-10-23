def parse_auth_header(header):
    try:
        return dict(map(_make_key_value, header.split(' ', 1)[1].split(',')))
    except Exception:
        return {
            
        }