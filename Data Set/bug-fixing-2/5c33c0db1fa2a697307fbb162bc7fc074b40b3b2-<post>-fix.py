

def post(self, request, organization_id):
    try:
        organization = Organization.objects.get_from_cache(id=organization_id)
    except Organization.DoesNotExist:
        logger.error((PROVIDER_NAME + '.webhook.invalid-organization'), extra={
            'organization_id': organization_id,
        })
        return HttpResponse(status=400)
    body = six.binary_type(request.body)
    if (not body):
        logger.error((PROVIDER_NAME + '.webhook.missing-body'), extra={
            'organization_id': organization.id,
        })
        return HttpResponse(status=400)
    try:
        handler = self.get_handler(request.META['HTTP_X_EVENT_KEY'])
    except KeyError:
        logger.error((PROVIDER_NAME + '.webhook.missing-event'), extra={
            'organization_id': organization.id,
        })
        return HttpResponse(status=400)
    if (not handler):
        return HttpResponse(status=204)
    address_string = six.text_type(request.META['REMOTE_ADDR'])
    ip = ipaddress.ip_address(address_string)
    valid_ip = False
    for ip_range in BITBUCKET_IP_RANGES:
        if (ip in ip_range):
            valid_ip = True
            break
    if ((not valid_ip) and (address_string not in BITBUCKET_IPS)):
        logger.error((PROVIDER_NAME + '.webhook.invalid-ip-range'), extra={
            'organization_id': organization.id,
        })
        return HttpResponse(status=401)
    try:
        event = json.loads(body.decode('utf-8'))
    except JSONDecodeError:
        logger.error((PROVIDER_NAME + '.webhook.invalid-json'), extra={
            'organization_id': organization.id,
        }, exc_info=True)
        return HttpResponse(status=400)
    handler()(organization, event)
    return HttpResponse(status=204)
