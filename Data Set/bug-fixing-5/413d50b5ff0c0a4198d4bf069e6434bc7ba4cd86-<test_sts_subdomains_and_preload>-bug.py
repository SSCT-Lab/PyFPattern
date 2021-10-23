@override_settings(SECURE_HSTS_SECONDS=10886400, SECURE_HSTS_INCLUDE_SUBDOMAINS=True, SECURE_HSTS_PRELOAD=True)
def test_sts_subdomains_and_preload(self):
    '\n        With HSTS_SECONDS non-zero, SECURE_HSTS_INCLUDE_SUBDOMAINS and\n        SECURE_HSTS_PRELOAD True, the middleware adds a "Strict-Transport-Security"\n        header containing both the "includeSubDomains" and "preload" directives\n        to the response.\n        '
    response = self.process_response(secure=True)
    self.assertEqual(response['Strict-Transport-Security'], 'max-age=10886400; includeSubDomains; preload')