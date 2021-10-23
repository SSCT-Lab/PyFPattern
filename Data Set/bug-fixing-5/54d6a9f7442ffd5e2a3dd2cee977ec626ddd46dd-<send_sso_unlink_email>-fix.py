def send_sso_unlink_email(self, actor, provider):
    from sentry.utils.email import MessageBuilder
    from sentry.models import LostPasswordHash
    email = self.get_email()
    recover_uri = '{path}?{query}'.format(path=reverse('sentry-account-recover'), query=urlencode({
        'email': email,
    }))
    if (not self.user_id):
        return
    context = {
        'email': email,
        'recover_url': absolute_uri(recover_uri),
        'has_password': self.user.password,
        'organization': self.organization,
        'actor': actor,
        'provider': provider,
    }
    if (not self.user.password):
        password_hash = LostPasswordHash.for_user(self.user)
        context['set_password_url'] = password_hash.get_absolute_url(mode='set_password')
    msg = MessageBuilder(subject=('Action Required for %s' % (self.organization.name,)), template='sentry/emails/auth-sso-disabled.txt', html_template='sentry/emails/auth-sso-disabled.html', type='organization.auth_sso_disabled', context=context)
    msg.send_async([email])