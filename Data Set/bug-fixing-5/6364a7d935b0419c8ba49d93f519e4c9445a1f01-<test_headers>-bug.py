def test_headers(self):
    resp = self.client.get(self.path)
    assert (resp.status_code == 200), resp
    self.assertIn('*', resp['Access-Control-Allow-Origin'])
    self.assertIn('stale-if-error', resp['Cache-Control'])
    self.assertIn('stale-while-revalidate', resp['Cache-Control'])
    self.assertIn('s-maxage', resp['Cache-Control'])
    self.assertIn('max-age', resp['Cache-Control'])
    self.assertIn(('project/%s' % self.projectkey.project_id), resp['Surrogate-Key'])
    self.assertIn(('sdk/%s' % settings.JS_SDK_LOADER_SDK_VERSION), resp['Surrogate-Key'])
    self.assertIn('sdk-loader', resp['Surrogate-Key'])
    assert ('Content-Encoding' not in resp)
    assert ('Set-Cookie' not in resp)
    assert ('Vary' not in resp)