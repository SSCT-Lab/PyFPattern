@override_settings(SECURE_SSL_REDIRECT=True)
def test_ssl_redirect_on(self):
    '\n        With SSL_REDIRECT True, the middleware redirects any non-secure\n        requests to the https:// version of the same URL.\n        '
    ret = self.process_request('get', '/some/url?query=string')
    self.assertEqual(ret.status_code, 301)
    self.assertEqual(ret['Location'], 'https://testserver/some/url?query=string')