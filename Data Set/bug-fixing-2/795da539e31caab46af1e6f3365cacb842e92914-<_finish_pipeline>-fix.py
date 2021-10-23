

def _finish_pipeline(self, data):
    if ('expect_exists' in data):
        integration = Integration.objects.get(provider=self.provider.key, external_id=data['external_id'])
    else:
        integration = ensure_integration(self.provider.key, data)
    org_integration = integration.add_organization(self.organization.id)
    identity = data.get('user_identity')
    identity_config = data.get('identity_config', {
        
    })
    if identity:
        (idp, created) = IdentityProvider.objects.get_or_create(external_id=data['external_id'], type=identity['type'], defaults={
            'config': identity_config,
        })
        if (not created):
            idp.update(config=identity_config)
        identity_data = {
            'status': IdentityStatus.VALID,
            'scopes': identity['scopes'],
            'data': identity['data'],
            'date_verified': timezone.now(),
        }
        try:
            (ident, created) = Identity.objects.get_or_create(idp=idp, user=self.request.user, external_id=identity['external_id'], defaults=identity_data)
            if (not created):
                ident.update(data=identity['data'], scopes=identity['scopes'])
        except IntegrityError:
            lookup = (Q(external_id=identity['external_id']) | Q(user=self.request.user))
            Identity.objects.filter(lookup, idp=idp).delete()
            Identity.objects.create(idp=idp, user=self.request.user, external_id=identity['external_id'], **identity_data)
    return self._dialog_response(serialize(org_integration, self.request.user), True)
