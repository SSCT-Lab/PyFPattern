@instrumented_task(name='sentry.tasks.store.preprocess_event', queue='events', time_limit=65, soft_time_limit=60)
def preprocess_event(cache_key=None, data=None, start_time=None, **kwargs):
    from sentry.plugins import plugins
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
    project = data['project']
    Raven.tags_context({
        'project': project,
    })
    has_changed = False
    for plugin in plugins.all(version=2):
        processors = safe_execute(plugin.get_event_preprocessors, _with_transaction=False)
        for processor in (processors or ()):
            result = safe_execute(processor, data)
            if result:
                data = result
                has_changed = True
    assert (data['project'] == project), 'Project cannot be mutated by preprocessor'
    if (has_changed and cache_key):
        default_cache.set(cache_key, data, 3600)
    if cache_key:
        data = None
    save_event.delay(cache_key=cache_key, data=data, start_time=start_time)