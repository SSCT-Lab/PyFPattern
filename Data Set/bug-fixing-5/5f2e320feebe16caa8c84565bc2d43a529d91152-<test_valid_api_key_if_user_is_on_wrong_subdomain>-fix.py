def test_valid_api_key_if_user_is_on_wrong_subdomain(self):
    with self.settings(REALMS_HAVE_SUBDOMAINS=True):
        with self.settings(RUNNING_INSIDE_TORNADO=False):
            with mock.patch('logging.warning') as mock_warning:
                with self.assertRaisesRegex(JsonableError, 'Account is not associated with this subdomain'):
                    validate_api_key(HostRequestMock(host=settings.EXTERNAL_HOST), self.default_bot.email, self.default_bot.api_key)
                mock_warning.assert_called_with('User {} attempted to access API on wrong subdomain {}'.format(self.default_bot.email, ''))
            with mock.patch('logging.warning') as mock_warning:
                with self.assertRaisesRegex(JsonableError, 'Account is not associated with this subdomain'):
                    validate_api_key(HostRequestMock(host=('acme.' + settings.EXTERNAL_HOST)), self.default_bot.email, self.default_bot.api_key)
                mock_warning.assert_called_with('User {} attempted to access API on wrong subdomain {}'.format(self.default_bot.email, 'acme'))