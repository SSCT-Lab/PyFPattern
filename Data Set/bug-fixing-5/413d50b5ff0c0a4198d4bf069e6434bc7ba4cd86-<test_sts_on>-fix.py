@override_settings(SECURE_HSTS_SECONDS=3600)
def test_sts_on(self):
    '\n        With SECURE_HSTS_SECONDS=3600, the middleware adds\n        "Strict-Transport-Security: max-age=3600" to the response.\n        '
    self.assertEqual(self.process_response(secure=True)['Strict-Transport-Security'], 'max-age=3600')