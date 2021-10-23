def process(self, request, project, key, auth, helper, data, project_config, attachments=None, **kwargs):
    disable_transaction_events()
    metrics.incr('events.total', skip_internal=False)
    project_id = project_config.project_id
    organization_id = project_config.organization_id
    if (not data):
        track_outcome(organization_id, project_id, key.id, Outcome.INVALID, 'no_data')
        raise APIError('No JSON data was found')
    remote_addr = request.META['REMOTE_ADDR']
    event_manager = EventManager(data, project=project, key=key, auth=auth, client_ip=remote_addr, user_agent=helper.context.agent, version=auth.version, content_encoding=request.META.get('HTTP_CONTENT_ENCODING', ''), project_config=project_config)
    del data
    self.pre_normalize(event_manager, helper)
    event_manager.normalize()
    data = event_manager.get_data()
    dict_data = dict(data)
    data_size = len(json.dumps(dict_data))
    if (data_size > 10000000):
        metrics.timing('events.size.rejected', data_size)
        track_outcome(organization_id, project_id, key.id, Outcome.INVALID, 'too_large', event_id=dict_data.get('event_id'))
        raise APIForbidden('Event size exceeded 10MB after normalization.')
    metrics.timing('events.size.data.post_storeendpoint', data_size)
    return process_event(event_manager, project, key, remote_addr, helper, attachments, project_config)