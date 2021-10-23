

def get(self, request, organization):
    has_catchall = features.has('organizations:internal-catchall', organization, actor=request.user)
    has_github_apps = features.has('organizations:github-apps', organization, actor=request.user)
    providers = []
    for provider in integrations.all():
        internal_integrations = {i for i in settings.SENTRY_INTERNAL_INTEGRATIONS if ((i != 'github') or (not has_github_apps))}
        if ((not has_catchall) and (provider.key in internal_integrations)):
            continue
        providers.append(provider)
    serialized = serialize(providers, organization=organization, serializer=IntegrationProviderSerializer())
    return Response({
        'providers': serialized,
    })
