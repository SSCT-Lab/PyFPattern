@never_cache
def post(self, request):
    grant_type = request.POST.get('grant_type')
    if (grant_type == 'authorization_code'):
        client_id = request.POST.get('client_id')
        client_secret = request.POST.get('client_secret')
        redirect_uri = request.POST.get('redirect_uri')
        code = request.POST.get('code')
        if (not client_id):
            return self.error(request, 'invalid_client', 'missing client_id')
        if (not client_secret):
            return self.error(request, 'invalid_client', 'missing client_secret')
        try:
            application = ApiApplication.objects.get(client_id=client_id, status=ApiApplicationStatus.active)
        except ApiApplication.DoesNotExist:
            return self.error(request, 'invalid_client', 'invalid client_id')
        if (not constant_time_compare(client_secret, application.client_secret)):
            return self.error(request, 'invalid_client', 'invalid client_secret')
        try:
            grant = ApiGrant.objects.get(application=application, code=code)
        except ApiGrant.DoesNotExist:
            return self.error(request, 'invalid_grant', 'invalid grant')
        if grant.is_expired():
            return self.error(request, 'invalid_grant', 'grant expired')
        if (not redirect_uri):
            redirect_uri = application.get_default_redirect_uri()
        elif (grant.redirect_uri != redirect_uri):
            return self.error(request, 'invalid_grant', 'invalid redirect_uri')
        token = ApiToken.from_grant(grant)
    elif (grant_type == 'refresh_token'):
        refresh_token = request.POST.get('refresh_token')
        scope = request.POST.get('scope')
        client_id = request.POST.get('client_id')
        client_secret = request.POST.get('client_secret')
        if (not refresh_token):
            return self.error(request, 'invalid_request')
        if scope:
            return self.error(request, 'invalid_request')
        if (not client_id):
            return self.error(request, 'invalid_client', 'missing client_id')
        if (not client_secret):
            return self.error(request, 'invalid_client', 'missing client_secret')
        try:
            application = ApiApplication.objects.get(client_id=client_id, status=ApiApplicationStatus.active)
        except ApiApplication.DoesNotExist:
            return self.error(request, 'invalid_client', 'invalid client_id')
        if (not constant_time_compare(client_secret, application.client_secret)):
            return self.error(request, 'invalid_client', 'invalid client_secret')
        try:
            token = ApiToken.objects.get(application=application, refresh_token=refresh_token)
        except ApiToken.DoesNotExist:
            return self.error(request, 'invalid_grant', 'invalid token')
        token.refresh()
    else:
        return self.error(request, 'unsupported_grant_type')
    return HttpResponse(json.dumps({
        'access_token': token.token,
        'refresh_token': token.refresh_token,
        'expires_in': (timezone.now() - token.expires_at).total_seconds(),
        'expires_at': token.expires_at,
        'token_type': 'bearer',
        'scope': ' '.join(token.get_scopes()),
        'user': {
            'id': six.text_type(token.user.id),
            'name': token.user.name,
            'email': token.user.email,
        },
    }), content_type='application/json')