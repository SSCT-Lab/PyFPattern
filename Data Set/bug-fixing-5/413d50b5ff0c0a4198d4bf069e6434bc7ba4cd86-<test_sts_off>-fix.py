@override_settings(SECURE_HSTS_SECONDS=0)
def test_sts_off(self):
    '\n        With SECURE_HSTS_SECONDS=0, the middleware does not add a\n        "Strict-Transport-Security" header to the response.\n        '
    self.assertNotIn('Strict-Transport-Security', self.process_response(secure=True))