def dispatch(self, request, organization, **kwargs):
    if self.needs_auth(request.user):
        return Response({
            'error_type': 'auth',
            'auth_url': reverse('socialauth_associate', args=[self.auth_provider]),
        }, status=400)
    try:
        fields = self.get_config()
    except Exception as e:
        return self.handle_api_error(e)
    if (request.method == 'GET'):
        return Response(fields)
    validator = ConfigValidator(fields, request.DATA)
    if (not validator.is_valid()):
        return Response({
            'error_type': 'validation',
            'errors': validator.errors,
        }, status=400)
    try:
        config = self.validate_config(organization, validator.result, actor=request.user)
    except Exception as e:
        return self.handle_api_error(e)
    try:
        result = self.create_repository(organization=organization, data=config, actor=request.user)
    except PluginError as e:
        return Response({
            'errors': {
                '__all__': e.message,
            },
        }, status=400)
    repo = Repository.objects.create(organization_id=organization.id, name=result['name'], external_id=result.get('external_id'), url=result.get('url'), config=(result.get('config') or {
        
    }), provider=self.id)
    return Response(serialize(repo, request.user), status=201)