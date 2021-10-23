def _do_preprocess_event(cache_key, data, start_time, event_id, process_event):
    if cache_key:
        data = default_cache.get(cache_key)
    if (data is None):
        metrics.incr('events.failed', tags={
            'reason': 'cache',
            'stage': 'pre',
        })
        error_logger.error('preprocess.failed.empty', extra={
            'cache_key': cache_key,
        })
        return
    project_id = data['project']
    Raven.tags_context({
        'project': project_id,
    })
    if should_process(data):
        hash_cache.set(get_raw_cache_key(project_id, data['event_id']), data)
        process_event.delay(cache_key=cache_key, start_time=start_time, event_id=event_id)
        return
    if cache_key:
        data = None
    save_event.delay(cache_key=cache_key, data=data, start_time=start_time, event_id=event_id)