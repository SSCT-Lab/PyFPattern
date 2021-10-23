@csrf_exempt
@never_cache
def dispatch(self, request, project_id=None, *args, **kwargs):
    helper = self.helper_cls(agent=request.META.get('HTTP_USER_AGENT'), project_id=project_id, ip_address=request.META['REMOTE_ADDR'])
    origin = None
    if (kafka_publisher is not None):
        self._publish_to_kafka(request)
    try:
        origin = helper.origin_from_request(request)
        response = self._dispatch(request, helper, *args, project_id=project_id, origin=origin, **kwargs)
    except APIError as e:
        context = {
            'error': force_bytes(e.msg, errors='replace'),
        }
        if e.name:
            context['error_name'] = e.name
        response = HttpResponse(json.dumps(context), content_type='application/json', status=e.http_status)
        response['X-Sentry-Error'] = context['error']
        if (isinstance(e, APIRateLimited) and (e.retry_after is not None)):
            response['Retry-After'] = six.text_type(int(math.ceil(e.retry_after)))
    except Exception as e:
        if settings.DEBUG:
            content = traceback.format_exc()
        else:
            content = ''
        logger.exception(e)
        response = HttpResponse(content, content_type='text/plain', status=500)
    metrics.incr('client-api.all-versions.requests')
    metrics.incr(('client-api.all-versions.responses.%s' % (response.status_code,)))
    metrics.incr(('client-api.all-versions.responses.%sxx' % (six.text_type(response.status_code)[0],)))
    if helper.context.version:
        metrics.incr(('client-api.v%s.requests' % (helper.context.version,)))
        metrics.incr(('client-api.v%s.responses.%s' % (helper.context.version, response.status_code)))
        metrics.incr(('client-api.v%s.responses.%sxx' % (helper.context.version, six.text_type(response.status_code)[0])))
    if ((response.status_code != 200) and origin):
        response['Access-Control-Allow-Origin'] = '*'
    if origin:
        response['Access-Control-Allow-Headers'] = 'X-Sentry-Auth, X-Requested-With, Origin, Accept, Content-Type, Authentication'
        response['Access-Control-Allow-Methods'] = ', '.join(self._allowed_methods())
        response['Access-Control-Expose-Headers'] = 'X-Sentry-Error, Retry-After'
    return response