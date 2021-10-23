def _parse_user_agent(data):
    http = data.get('request')
    if (not http):
        return None
    headers = http.get('headers')
    if (not headers):
        return None
    try:
        for (key, value) in headers:
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