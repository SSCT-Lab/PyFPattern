def test_validate_basic(self):
    report = {
        'document-uri': 'http://45.55.25.245:8123/csp',
        'referrer': 'http://example.com',
        'violated-directive': 'img-src https://45.55.25.245:8123/',
        'effective-directive': 'img-src',
        'original-policy': "default-src  https://45.55.25.245:8123/; child-src  https://45.55.25.245:8123/; connect-src  https://45.55.25.245:8123/; font-src  https://45.55.25.245:8123/; img-src  https://45.55.25.245:8123/; media-src  https://45.55.25.245:8123/; object-src  https://45.55.25.245:8123/; script-src  https://45.55.25.245:8123/; style-src  https://45.55.25.245:8123/; form-action  https://45.55.25.245:8123/; frame-ancestors 'none'; plugin-types 'none'; report-uri http://45.55.25.245:8123/csp-report?os=OS%20X&device=&browser_version=43.0&browser=chrome&os_version=Lion",
        'blocked-uri': 'http://google.com',
        'status-code': 200,
        '_meta': {
            'release': 'abc123',
        },
    }
    result = self.helper.validate_data(self.project, report)
    assert (result['logger'] == 'csp')
    assert (result['project'] == self.project.id)
    assert (result['release'] == 'abc123')
    assert (result['errors'] == [])
    assert ('message' in result)
    assert ('culprit' in result)
    assert (result['tags'] == [('effective-directive', 'img-src'), ('blocked-uri', 'http://google.com')])
    assert (result['sentry.interfaces.User'] == {
        'ip_address': '69.69.69.69',
    })
    assert (result['sentry.interfaces.Http'] == {
        'url': 'http://45.55.25.245:8123/csp',
        'headers': {
            'User-Agent': 'Awesome Browser',
            'Referer': 'http://example.com',
        },
    })