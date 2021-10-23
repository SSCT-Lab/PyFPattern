def post(self, request, organization):
    if (not request.user.is_authenticated()):
        return Response(status=401)
    if (not self.has_feature(request, organization)):
        return self.respond({
            'error_type': 'unavailable_feature',
            'detail': ['You do not have that feature enabled'],
        }, status=403)
    provider_id = request.DATA.get('provider')
    has_ghe = ((provider_id == 'integrations:github_enterprise') and features.has('organizations:github-enterprise', organization, actor=request.user))
    has_bb = ((provider_id == 'integrations:bitbucket') and features.has('organizations:bitbucket-integration', organization, actor=request.user))
    has_vsts = ((provider_id == 'integrations:vsts') and features.has('organizations:vsts-integration', organization, actor=request.user))
    has_github = ((provider_id == 'integrations:github') and features.has('organizations:github-apps', organization, actor=request.user))
    if (features.has('organizations:internal-catchall', organization, actor=request.user) or has_ghe or has_bb or has_vsts or has_github):
        if ((provider_id is not None) and provider_id.startswith('integrations:')):
            try:
                provider_cls = bindings.get('integration-repository.provider').get(provider_id)
            except KeyError:
                return Response({
                    'error_type': 'validation',
                }, status=400)
            provider = provider_cls(id=provider_id)
            return provider.dispatch(request, organization)
    try:
        provider_cls = bindings.get('repository.provider').get(provider_id)
    except KeyError:
        return Response({
            'error_type': 'validation',
        }, status=400)
    provider = provider_cls(id=provider_id)
    return provider.dispatch(request, organization)