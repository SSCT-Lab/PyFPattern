def get_all_keys(session):
    url = (API_BASE + '/user/keys')
    result = []
    while url:
        r = session.request('GET', url)
        result.extend(r.json())
        url = r.links().get('next')
    return result