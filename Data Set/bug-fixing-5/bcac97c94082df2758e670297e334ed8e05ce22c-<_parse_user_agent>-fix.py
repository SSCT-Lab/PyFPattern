def _parse_user_agent(data):
    try:
        for (key, value) in (get_path(data, 'request', 'headers', filter=True) or ()):
            if (key != 'User-Agent'):
                continue
            if (not value):
                continue
            ua = Parse(value)
            if (not ua):
                continue
            return ua
    except ValueError:
        pass
    return None