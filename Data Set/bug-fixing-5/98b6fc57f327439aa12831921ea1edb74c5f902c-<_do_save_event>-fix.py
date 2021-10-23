def _do_save_event(cache_key=None, data=None, start_time=None, event_id=None, project_id=None, **kwargs):
    '\n    Saves an event to the database.\n    '
    from sentry.event_manager import HashDiscarded, EventManager
    from sentry import quotas
    from sentry.models import ProjectKey
    from sentry.utils.outcomes import Outcome, track_outcome
    from sentry.ingest.outcomes_consumer import mark_signal_sent
    if (cache_key and (data is None)):
        data = default_cache.get(cache_key)
    if (data is not None):
        data = CanonicalKeyDict(data)
    if ((event_id is None) and (data is not None)):
        event_id = data['event_id']
    if (project_id is None):
        project_id = data.pop('project')
    key_id = (None if (data is None) else data.get('key_id'))
    if (key_id is not None):
        key_id = int(key_id)
    timestamp = (to_datetime(start_time) if (start_time is not None) else None)
    if ((not data) or reprocessing.event_supports_reprocessing(data)):
        delete_raw_event(project_id, event_id, allow_hint_clear=True)
    if (not data):
        metrics.incr('events.failed', tags={
            'reason': 'cache',
            'stage': 'post',
        }, skip_internal=False)
        return
    with configure_scope() as scope:
        scope.set_tag('project', project_id)
    event = None
    try:
        manager = EventManager(data)
        event = manager.save(project_id, assume_normalized=True)
        if features.has('organizations:event-attachments', event.project.organization, actor=None):
            attachments = (attachment_cache.get(cache_key) or [])
            for attachment in attachments:
                save_attachment(event, attachment)
        track_outcome(event.project.organization_id, event.project.id, key_id, Outcome.ACCEPTED, None, timestamp, event_id)
    except HashDiscarded:
        project = Project.objects.get_from_cache(id=project_id)
        reason = FilterStatKeys.DISCARDED_HASH
        project_key = None
        try:
            if (key_id is not None):
                project_key = ProjectKey.objects.get_from_cache(id=key_id)
        except ProjectKey.DoesNotExist:
            pass
        quotas.refund(project, key=project_key, timestamp=start_time)
        mark_signal_sent(event_id, project_id)
        track_outcome(project.organization_id, project_id, key_id, Outcome.FILTERED, reason, timestamp, event_id)
    finally:
        if cache_key:
            default_cache.delete(cache_key)
            if ((event is None) or features.has('organizations:event-attachments', event.project.organization, actor=None)):
                attachment_cache.delete(cache_key)
        if start_time:
            metrics.timing('events.time-to-process', (time() - start_time), instance=data['platform'])