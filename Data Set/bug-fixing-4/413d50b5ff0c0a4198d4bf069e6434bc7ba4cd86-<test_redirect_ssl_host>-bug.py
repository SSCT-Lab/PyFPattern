@override_settings(SECURE_SSL_REDIRECT=True, SECURE_SSL_HOST='secure.example.com')
def test_redirect_ssl_host(self):
    '\n        The middleware redirects to SSL_HOST if given.\n        '
    ret = self.process_request('get', '/some/url')
    self.assertEqual(ret.status_code, 301)
    self.assertEqual(ret['Location'], 'https://secure.example.com/some/url')