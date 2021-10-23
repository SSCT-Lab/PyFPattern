@override_settings(SECURE_HSTS_SECONDS=600, SECURE_HSTS_INCLUDE_SUBDOMAINS=True)
def test_sts_include_subdomains(self):
    '\n        With SECURE_HSTS_SECONDS non-zero and SECURE_HSTS_INCLUDE_SUBDOMAINS\n        True, the middleware adds a "Strict-Transport-Security" header with the\n        "includeSubDomains" directive to the response.\n        '
    response = self.process_response(secure=True)
    self.assertEqual(response['Strict-Transport-Security'], 'max-age=600; includeSubDomains')