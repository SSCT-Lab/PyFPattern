def load_data(platform, default=None, timestamp=None, sample_name=None):
    data = None
    language = None
    platform_data = INTEGRATION_ID_TO_PLATFORM_DATA.get(platform)
    if ((platform_data is not None) and (platform_data['type'] != 'language')):
        language = platform_data['language']
    for platform in (platform, language, default):
        if (not platform):
            continue
        json_path = os.path.join(DATA_ROOT, 'samples', ('%s.json' % (platform.encode('utf-8'),)))
        if (not os.path.exists(json_path)):
            continue
        if (not sample_name):
            try:
                sample_name = INTEGRATION_ID_TO_PLATFORM_DATA[platform]['name']
            except KeyError:
                pass
        with open(json_path) as fp:
            data = json.loads(fp.read())
            break
    if (data is None):
        return
    data = CanonicalKeyDict(data)
    if (platform in ('csp', 'hkpk', 'expectct', 'expectstaple')):
        return data
    data['platform'] = platform
    data['message'] = ('This is an example %s exception' % ((sample_name or platform),))
    data['user'] = generate_user(ip_address='127.0.0.1', username='sentry', id=1, email='sentry@example.com')
    data['extra'] = {
        'session': {
            'foo': 'bar',
        },
        'results': [1, 2, 3, 4, 5],
        'emptyList': [],
        'emptyMap': {
            
        },
        'length': 10837790,
        'unauthorized': False,
        'url': 'http://example.org/foo/bar/',
    }
    data['modules'] = {
        'my.package': '1.0.0',
    }
    data['request'] = {
        'cookies': 'foo=bar;biz=baz',
        'url': 'http://example.com/foo',
        'headers': {
            'Referer': 'http://example.com',
            'Content-Type': 'application/json',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.72 Safari/537.36',
        },
        'env': {
            'ENV': 'prod',
        },
        'query_string': 'foo=bar',
        'data': '{"hello": "world"}',
        'method': 'GET',
    }
    start = datetime.utcnow()
    if timestamp:
        try:
            start = datetime.utcfromtimestamp(timestamp)
        except TypeError:
            pass
    breadcrumbs = data.get('breadcrumbs')
    if (breadcrumbs is not None):
        duration = 1000
        values = ((isinstance(breadcrumbs, list) and breadcrumbs) or breadcrumbs['values'])
        for value in reversed(values):
            value['timestamp'] = milliseconds_ago(start, duration)
            duration += 1000
    return data