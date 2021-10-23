@classmethod
def normalize_crumb(cls, crumb):
    ty = (crumb.get('type') or 'default')
    level = crumb.get('level')
    if ((not isinstance(level, six.string_types)) or ((level not in LOG_LEVELS_MAP) and (level != 'critical'))):
        level = 'info'
    ts = parse_timestamp(crumb.get('timestamp'))
    if (ts is None):
        raise InterfaceValidationError('Unable to determine timestamp for crumb')
    ts = to_timestamp(ts)
    msg = crumb.get('message')
    if (msg is not None):
        msg = trim(six.text_type(msg), 4096)
    category = crumb.get('category')
    if (category is not None):
        category = trim(six.text_type(category), 256)
    event_id = crumb.get('event_id')
    data = crumb.get('data')
    if (not isinstance(data, dict)):
        data = None
    else:
        data = trim(data, 4096)
    return {
        'type': ty,
        'level': level,
        'timestamp': ts,
        'message': msg,
        'category': category,
        'event_id': event_id,
        'data': data,
    }