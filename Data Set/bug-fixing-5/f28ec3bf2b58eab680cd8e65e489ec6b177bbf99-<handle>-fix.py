@never_cache
def handle(self, request, signed_params):
    params = unsign(signed_params.encode('ascii', errors='ignore'))
    try:
        organization = Organization.objects.get(id__in=request.user.get_orgs(), id=params['organization_id'])
    except Organization.DoesNotExist:
        raise Http404
    try:
        integration = Integration.objects.get(id=params['integration_id'], organizations=organization)
    except Integration.DoesNotExist:
        raise Http404
    try:
        idp = IdentityProvider.objects.get(type='slack', organization=organization)
    except Integration.DoesNotExist:
        raise Http404
    if (request.method != 'POST'):
        return render_to_response('sentry/auth-link-identity.html', request=request, context={
            'organization': organization,
            'provider': integration.get_provider(),
        })
    (identity, created) = Identity.objects.get_or_create(user=request.user, idp=idp, defaults={
        'external_id': params['slack_id'],
        'status': IdentityStatus.VALID,
    })
    if (not created):
        identity.update(external_id=params['slack_id'], status=IdentityStatus.VALID)
    payload = {
        'replace_original': False,
        'response_type': 'ephemeral',
        'text': "Your Slack identity has been linked to your Sentry account. You're good to go!",
    }
    session = http.build_session()
    req = session.post(params['response_url'], json=payload)
    resp = req.json()
    if ((not resp.get('ok')) and (resp.get('error') != 'Expired url')):
        logger.error('slack.link-notify.response-error', extra={
            'response': resp,
        })
    return render_to_response('sentry/slack-linked.html', request=request, context={
        'channel_id': params['channel_id'],
        'team_id': integration.external_id,
    })