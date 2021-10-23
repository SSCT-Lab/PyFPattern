def process(self, request, project, key, auth, helper, data, attachments=None, **kwargs):
    metrics.incr('events.total', skip_internal=False)
    if (not data):
        raise APIError('No JSON data was found')
    remote_addr = request.META['REMOTE_ADDR']
    event_manager = EventManager(data, project=project, key=key, auth=auth, client_ip=remote_addr, user_agent=helper.context.agent, version=auth.version, content_encoding=request.META.get('HTTP_CONTENT_ENCODING', ''))
    del data
    self.pre_normalize(event_manager, helper)
    event_manager.normalize()
    return process_event(event_manager, project, key, remote_addr, helper, attachments)