

@override_settings(AUTHENTICATION_BACKENDS=('zproject.backends.ZulipLDAPAuthBackend',))
def test_query_email_attr(self) -> None:
    self._LDAPUser.attrs = {
        'cn': ['King Hamlet'],
        'sn': ['Hamlet'],
        'email_attr': ['separate_email@zulip.com'],
    }
    with self.settings(AUTH_LDAP_USER_ATTR_MAP={
        'full_name': 'cn',
        'short_name': 'sn',
    }, LDAP_EMAIL_ATTR='email_attr'), mock.patch('zproject.backends._LDAPUser', self._LDAPUser, create=True):
        values = query_ldap(self.example_email('hamlet'))
    self.assertEqual(len(values), 3)
    self.assertIn('full_name: King Hamlet', values)
    self.assertIn('short_name: Hamlet', values)
    self.assertIn('email: separate_email@zulip.com', values)
