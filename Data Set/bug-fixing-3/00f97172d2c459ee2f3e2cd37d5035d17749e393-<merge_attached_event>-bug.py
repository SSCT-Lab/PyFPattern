def merge_attached_event(mpack_event, data):
    '\n    Merges an event payload attached in the ``__sentry-event`` attachment.\n    '
    size = mpack_event.size
    if ((size == 0) or (size > MAX_MSGPACK_EVENT_SIZE_BYTES)):
        return
    try:
        event = unpack(mpack_event)
    except (ValueError, UnpackException, ExtraData) as e:
        minidumps_logger.exception(e)
        return
    for key in event:
        value = event.get(key)
        if (value is not None):
            data[key] = value