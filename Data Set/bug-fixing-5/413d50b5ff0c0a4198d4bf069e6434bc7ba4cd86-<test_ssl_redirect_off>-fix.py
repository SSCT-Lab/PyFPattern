@override_settings(SECURE_SSL_REDIRECT=False)
def test_ssl_redirect_off(self):
    '\n        With SECURE_SSL_REDIRECT False, the middleware does not redirect.\n        '
    ret = self.process_request('get', '/some/url')
    self.assertIsNone(ret)