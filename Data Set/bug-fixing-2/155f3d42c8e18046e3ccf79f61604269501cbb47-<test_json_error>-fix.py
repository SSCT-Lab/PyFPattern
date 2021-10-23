

@mock.patch('zerver.lib.request._')
def test_json_error(self, mock_gettext):
    dummy_value = "this arg is bad: '%s' (translated to German)"
    mock_gettext.return_value = dummy_value
    email = self.example_email('hamlet')
    self.login(email)
    result = self.client_post('/json/invite_users', HTTP_ACCEPT_LANGUAGE='de')
    expected_error = "this arg is bad: 'invitee_emails' (translated to German)"
    self.assert_json_error_contains(result, expected_error, status_code=400)
