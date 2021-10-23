@mock.patch('zerver.lib.request._')
def test_json_error(self, mock_gettext):
    dummy_value = "Some other language '%s'"
    mock_gettext.return_value = dummy_value
    email = self.example_email('hamlet')
    self.login(email)
    result = self.client_post('/json/refer_friend', HTTP_ACCEPT_LANGUAGE='de')
    self.assert_json_error_contains(result, (dummy_value % 'email'), status_code=400)