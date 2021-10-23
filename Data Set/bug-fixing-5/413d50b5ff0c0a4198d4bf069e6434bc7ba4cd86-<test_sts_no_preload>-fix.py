@override_settings(SECURE_HSTS_SECONDS=10886400, SECURE_HSTS_PRELOAD=False)
def test_sts_no_preload(self):
    '\n        With SECURE_HSTS_SECONDS non-zero and SECURE_HSTS_PRELOAD\n        False, the middleware adds a "Strict-Transport-Security" header without\n        the "preload" directive to the response.\n        '
    response = self.process_response(secure=True)
    self.assertEqual(response['Strict-Transport-Security'], 'max-age=10886400')