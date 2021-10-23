

@instrumented_task(name='sentry.tasks.unmerge', queue='unmerge')
def unmerge(project_id, source_id, destination_id, fingerprints, actor_id, last_event=None, batch_size=500, source_fields_reset=False, eventstream_state=None):
    source = Group.objects.get(project_id=project_id, id=source_id)
    if (last_event is None):
        fingerprints = lock_hashes(project_id, source_id, fingerprints)
        truncate_denormalizations(source)
    caches = get_caches()
    project = caches['Project'](project_id)
    conditions = []
    if (last_event is not None):
        conditions.extend([['timestamp', '<=', last_event.timestamp], [['timestamp', '<', last_event.timestamp], ['event_id', '<', last_event.event_id]]])
    events = eventstore.get_events(filter_keys={
        'project_id': [project_id],
        'issue': [source.id],
    }, additional_columns=[eventstore.Columns.MESSAGE], conditions=conditions, limit=batch_size, referrer='unmerge', orderby=['-timestamp', '-event_id'])
    if (not events):
        tagstore.update_group_tag_key_values_seen(project_id, [source_id, destination_id])
        unlock_hashes(project_id, fingerprints)
        logger.warning('Unmerge complete (eventstream state: %s)', eventstream_state)
        if eventstream_state:
            eventstream.end_unmerge(eventstream_state)
        return destination_id
    Event.objects.bind_nodes(events, 'data')
    source_events = []
    destination_events = []
    for event in events:
        (destination_events if (get_fingerprint(event) in fingerprints) else source_events).append(event)
    if source_events:
        if (not source_fields_reset):
            source.update(**get_group_creation_attributes(caches, source_events))
            source_fields_reset = True
        else:
            source.update(**get_group_backfill_attributes(caches, source, source_events))
    (destination_id, eventstream_state) = migrate_events(caches, project, source_id, destination_id, fingerprints, destination_events, actor_id, eventstream_state)
    repair_denormalizations(caches, project, events)
    unmerge.delay(project_id, source_id, destination_id, fingerprints, actor_id, last_event=events[(- 1)], batch_size=batch_size, source_fields_reset=source_fields_reset, eventstream_state=eventstream_state)
