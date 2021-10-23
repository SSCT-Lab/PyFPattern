@override_settings(SECURE_BROWSER_XSS_FILTER=True)
def test_xss_filter_on(self):
    '\n        With BROWSER_XSS_FILTER set to True, the middleware adds\n        "s-xss-protection: 1; mode=block" header to the response.\n        '
    self.assertEqual(self.process_response()['X-XSS-Protection'], '1; mode=block')