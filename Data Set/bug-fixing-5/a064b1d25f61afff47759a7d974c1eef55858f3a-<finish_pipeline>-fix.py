def finish_pipeline(self):
    identity = self.provider.build_identity(self.state.data)
    defaults = {
        'status': IdentityStatus.VALID,
        'scopes': identity.get('scopes', []),
        'data': identity.get('data', {
            
        }),
        'date_verified': timezone.now(),
    }
    (identity, created) = Identity.objects.get_or_create(idp=self.provider_model, user=self.request.user, external_id=identity['id'], defaults=defaults)
    if (not created):
        identity.update(**defaults)
    messages.add_message(self.request, messages.SUCCESS, IDENTITY_LINKED.format(identity_provider=self.provider.name))
    self.state.clear()
    return HttpResponseRedirect(reverse('sentry-account-settings'))