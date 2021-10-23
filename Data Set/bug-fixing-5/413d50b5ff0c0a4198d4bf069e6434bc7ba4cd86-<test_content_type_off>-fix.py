@override_settings(SECURE_CONTENT_TYPE_NOSNIFF=False)
def test_content_type_off(self):
    '\n        With SECURE_CONTENT_TYPE_NOSNIFF False, the middleware does not add an\n        "X-Content-Type-Options" header to the response.\n        '
    self.assertNotIn('X-Content-Type-Options', self.process_response())