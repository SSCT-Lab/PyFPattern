@override_settings(SECURE_HSTS_SECONDS=10886400, SECURE_HSTS_PRELOAD=True)
def test_sts_preload(self):
    '\n        With SECURE_HSTS_SECONDS non-zero and SECURE_HSTS_PRELOAD True, the\n        middleware adds a "Strict-Transport-Security" header with the "preload"\n        directive to the response.\n        '
    response = self.process_response(secure=True)
    self.assertEqual(response['Strict-Transport-Security'], 'max-age=10886400; preload')