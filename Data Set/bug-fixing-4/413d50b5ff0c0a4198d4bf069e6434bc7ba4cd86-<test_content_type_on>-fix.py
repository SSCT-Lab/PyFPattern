@override_settings(SECURE_CONTENT_TYPE_NOSNIFF=True)
def test_content_type_on(self):
    '\n        With SECURE_CONTENT_TYPE_NOSNIFF set to True, the middleware adds\n        "X-Content-Type-Options: nosniff" header to the response.\n        '
    self.assertEqual(self.process_response()['X-Content-Type-Options'], 'nosniff')