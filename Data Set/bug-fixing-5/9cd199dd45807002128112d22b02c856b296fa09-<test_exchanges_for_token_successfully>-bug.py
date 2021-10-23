def test_exchanges_for_token_successfully(self):
    response = self._run_request()
    token = ApiToken.objects.get(application=self.sentry_app.application)
    assert (response.status_code == 201), response.content
    assert (response.data['scopes'] == self.sentry_app.scope_list)
    assert (response.data['token'] == token.token)
    assert (response.data['refreshToken'] == token.refresh_token)
    expires_at = response.data['expiresAt'].replace(second=0, microsecond=0)
    expected_expires_at = (datetime.now() + timedelta(hours=8)).replace(second=0, microsecond=0)
    assert (expires_at == expected_expires_at)