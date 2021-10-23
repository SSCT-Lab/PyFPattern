

def post(self, request):
    token = '<unknown>'
    try:
        token = request.META['HTTP_X_GITLAB_TOKEN']
        (instance, group_path, secret) = token.split(':')
        external_id = '{}:{}'.format(instance, group_path)
    except Exception:
        logger.info('gitlab.webhook.invalid-token', extra={
            'token': token,
        })
        return HttpResponse(status=400)
    try:
        integration = Integration.objects.filter(provider=self.provider, external_id=external_id).prefetch_related('organizations').get()
    except Integration.DoesNotExist:
        logger.info('gitlab.webhook.invalid-organization', extra={
            'external_id': request.META['HTTP_X_GITLAB_TOKEN'],
        })
        return HttpResponse(status=400)
    if (not constant_time_compare(secret, integration.metadata['webhook_secret'])):
        logger.info('gitlab.webhook.invalid-token-secret', extra={
            'integration_id': integration.id,
        })
        return HttpResponse(status=400)
    try:
        event = json.loads(request.body.decode('utf-8'))
    except JSONDecodeError:
        logger.info('gitlab.webhook.invalid-json', extra={
            'external_id': integration.external_id,
        })
        return HttpResponse(status=400)
    try:
        handler = self._handlers[request.META['HTTP_X_GITLAB_EVENT']]
    except KeyError:
        logger.info('gitlab.webhook.missing-event', extra={
            'event': request.META['HTTP_X_GITLAB_EVENT'],
        })
        return HttpResponse(status=400)
    for organization in integration.organizations.all():
        handler()(integration, organization, event)
    return HttpResponse(status=204)
