@patch('sentry.loader.browsersdkversion.load_version_from_file')
def test_headers(self, mock_load_version_from_file):
    mocked_version = '9.9.9'
    mock_load_version_from_file.return_value = mocked_version
    resp = self.client.get(self.path)
    assert (resp.status_code == 200), resp
    self.assertIn('*', resp['Access-Control-Allow-Origin'])
    self.assertIn('stale-if-error', resp['Cache-Control'])
    self.assertIn('stale-while-revalidate', resp['Cache-Control'])
    self.assertIn('s-maxage', resp['Cache-Control'])
    self.assertIn('max-age', resp['Cache-Control'])
    self.assertIn(('project/%s' % self.projectkey.project_id), resp['Surrogate-Key'])
    self.assertIn(('sdk/%s' % mocked_version), resp['Surrogate-Key'])
    self.assertIn('sdk-loader', resp['Surrogate-Key'])
    assert ('Content-Encoding' not in resp)
    assert ('Set-Cookie' not in resp)
    assert ('Vary' not in resp)