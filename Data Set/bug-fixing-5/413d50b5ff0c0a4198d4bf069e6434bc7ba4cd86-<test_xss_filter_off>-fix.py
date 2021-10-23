@override_settings(SECURE_BROWSER_XSS_FILTER=False)
def test_xss_filter_off(self):
    '\n        With SECURE_BROWSER_XSS_FILTER set to False, the middleware does not\n        add an "X-XSS-Protection" header to the response.\n        '
    self.assertNotIn('X-XSS-Protection', self.process_response())