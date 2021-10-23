

def _do_process_event(cache_key, start_time, event_id, process_task, data=None):
    from sentry.plugins.base import plugins
    if (data is None):
        data = default_cache.get(cache_key)
    if (data is None):
        metrics.incr('events.failed', tags={
            'reason': 'cache',
            'stage': 'process',
        }, skip_internal=False)
        error_logger.error('process.failed.empty', extra={
            'cache_key': cache_key,
        })
        return
    data = CanonicalKeyDict(data)
    project_id = data['project']
    with configure_scope() as scope:
        scope.set_tag('project', project_id)
    has_changed = False
    reprocessing_rev = reprocessing.get_reprocessing_revision(project_id)
    try:
        for plugin in plugins.all(version=2):
            enhancers = safe_execute(plugin.get_event_enhancers, data=data)
            for enhancer in (enhancers or ()):
                enhanced = safe_execute(enhancer, data, _passthrough_errors=(RetrySymbolication,))
                if enhanced:
                    data = enhanced
                    has_changed = True
        new_data = process_stacktraces(data)
        if (new_data is not None):
            has_changed = True
            data = new_data
    except RetrySymbolication as e:
        if (start_time and ((time() - start_time) > 3600)):
            error_logger.exception('process.failed.infinite_retry')
        else:
            retry_process_event.apply_async(args=(), kwargs={
                'process_task_name': process_task.__name__,
                'task_kwargs': {
                    'cache_key': cache_key,
                    'event_id': event_id,
                    'start_time': start_time,
                },
            }, countdown=e.retry_after)
            return
    for plugin in plugins.all(version=2):
        processors = safe_execute(plugin.get_event_preprocessors, data=data, _with_transaction=False)
        for processor in (processors or ()):
            result = safe_execute(processor, data)
            if result:
                data = result
                has_changed = True
    assert (data['project'] == project_id), 'Project cannot be mutated by preprocessor'
    project = Project.objects.get_from_cache(id=project_id)
    if isinstance(data, CANONICAL_TYPES):
        data = dict(data.items())
    if has_changed:
        normalizer = StoreNormalizer(remove_other=False, is_renormalize=True, **DEFAULT_STORE_NORMALIZER_ARGS)
        data = normalizer.normalize_event(dict(data))
        issues = data.get('processing_issues')
        try:
            if (issues and create_failed_event(cache_key, data, project_id, list(issues.values()), event_id=event_id, start_time=start_time, reprocessing_rev=reprocessing_rev)):
                return
        except RetryProcessing:
            from_reprocessing = (process_task is process_event_from_reprocessing)
            submit_process(project, from_reprocessing, cache_key, event_id, start_time, data)
            process_task.delay(cache_key, start_time=start_time, event_id=event_id)
            return
        default_cache.set(cache_key, data, 3600)
    submit_save_event(project, cache_key, event_id, start_time, data)
