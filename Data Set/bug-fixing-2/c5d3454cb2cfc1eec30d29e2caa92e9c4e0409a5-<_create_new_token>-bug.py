

def _create_new_token(self):
    token = ApiToken.objects.create(user=self.user, application=self.application, scope_list=self.sentry_app.scope_list, expires_at=token_expiration())
    self.install.api_token = token
    self.install.save()
    return token
