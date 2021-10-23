def get_task_kwargs_for_message(value):
    '\n    Decodes a message body, returning a dictionary of keyword arguments that\n    can be applied to a post-processing task, or ``None`` if no task should be\n    dispatched.\n    '
    metrics.timing('evenstream.events.size.data', len(value))
    payload = json.loads(value)
    event_id = get_path(payload, 2, 'event_id')
    project_id = get_path(payload, 2, 'project_id')
    metrics.incr(('evenstream.events.size.data.mb_bucket.%s' % ((len(value) // (10 ** 6)),)), tags={
        'project_id': (project_id or 'None'),
        'event': ('%s,%s' % (project_id, event_id)),
    })
    try:
        version = payload[0]
    except Exception:
        raise InvalidPayload('Received event payload with unexpected structure')
    try:
        handler = version_handlers[int(version)]
    except (ValueError, KeyError):
        raise InvalidVersion('Received event payload with unexpected version identifier: {}'.format(version))
    return handler(*payload[1:])