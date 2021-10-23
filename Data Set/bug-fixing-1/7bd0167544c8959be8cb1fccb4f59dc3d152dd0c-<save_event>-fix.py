

@instrumented_task(name='sentry.tasks.store.save_event', queue='events.save_event')
def save_event(cache_key=None, data=None, start_time=None, event_id=None, **kwargs):
    '\n    Saves an event to the database.\n    '
    from sentry.event_manager import HashDiscarded, EventManager
    if cache_key:
        data = default_cache.get(cache_key)
    if ((event_id is None) and (data is not None)):
        event_id = data['event_id']
    if (data is None):
        metrics.incr('events.failed', tags={
            'reason': 'cache',
            'stage': 'post',
        })
        return
    project = data.pop('project')
    delete_raw_event(project, event_id, allow_hint_clear=True)
    Raven.tags_context({
        'project': project,
    })
    try:
        manager = EventManager(data)
        manager.save(project)
    except HashDiscarded as exc:
        info_logger.info('discarded.hash', extra={
            'project_id': project,
            'message': exc.message,
        })
    finally:
        if cache_key:
            default_cache.delete(cache_key)
        if start_time:
            metrics.timing('events.time-to-process', (time() - start_time), instance=data['platform'])
