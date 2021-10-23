def get_all_keys(session):
    url = (API_BASE + '/user/keys')
    while url:
        r = session.request('GET', url)
        for key in r.json():
            (yield key)
        url = r.links().get('next')