def merge_attached_breadcrumbs(mpack_breadcrumbs, data):
    '\n    Merges breadcrumbs attached in the ``__sentry-breadcrumbs`` attachment(s).\n    '
    size = mpack_breadcrumbs.size
    if ((size == 0) or (size > MAX_MSGPACK_BREADCRUMB_SIZE_BYTES)):
        return
    try:
        unpacker = Unpacker(mpack_breadcrumbs)
        breadcrumbs = list(unpacker)
    except (TypeError, ValueError, UnpackException, ExtraData) as e:
        minidumps_logger.exception(e)
        return
    if (not breadcrumbs):
        return
    current_crumbs = data.get('breadcrumbs')
    if (not current_crumbs):
        data['breadcrumbs'] = breadcrumbs
        return
    current_crumb = next((c for c in reversed(current_crumbs) if (isinstance(c, dict) and (c.get('timestamp') is not None))), None)
    new_crumb = next((c for c in reversed(breadcrumbs) if (isinstance(c, dict) and (c.get('timestamp') is not None))), None)
    cap = max(len(current_crumbs), len(breadcrumbs))
    if ((current_crumb is not None) and (new_crumb is not None)):
        if (dp.parse(current_crumb['timestamp']) > dp.parse(new_crumb['timestamp'])):
            data['breadcrumbs'] = (breadcrumbs + current_crumbs)
        else:
            data['breadcrumbs'] = (current_crumbs + breadcrumbs)
    else:
        data['breadcrumbs'] = (current_crumbs + breadcrumbs)
    data['breadcrumbs'] = data['breadcrumbs'][(- cap):]