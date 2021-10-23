def track_outcome(org_id, project_id, key_id, outcome, reason=None, timestamp=None, event_id=None):
    '\n    This is a central point to track org/project counters per incoming event.\n    NB: This should only ever be called once per incoming event, which means\n    it should only be called at the point we know the final outcome for the\n    event (invalid, rate_limited, accepted, discarded, etc.)\n\n    This increments all the relevant legacy RedisTSDB counters, as well as\n    sending a single metric event to Kafka which can be used to reconstruct the\n    counters with SnubaTSDB.\n    '
    global outcomes_publisher
    if (outcomes_publisher is None):
        outcomes_publisher = KafkaPublisher(settings.KAFKA_CLUSTERS[outcomes['cluster']])
    assert isinstance(org_id, six.integer_types)
    assert isinstance(project_id, six.integer_types)
    assert isinstance(key_id, (type(None), six.integer_types))
    assert isinstance(outcome, Outcome)
    assert isinstance(timestamp, (type(None), datetime))
    timestamp = (timestamp or to_datetime(time.time()))
    tsdb_in_consumer = decide_tsdb_in_consumer()
    if (not tsdb_in_consumer):
        increment_list = list(tsdb_increments_from_outcome(org_id=org_id, project_id=project_id, key_id=key_id, outcome=outcome, reason=reason))
        if increment_list:
            tsdb.incr_multi(increment_list, timestamp=timestamp)
        if (project_id and event_id):
            mark_tsdb_incremented(project_id, event_id)
    outcomes_publisher.publish(outcomes['topic'], json.dumps({
        'timestamp': timestamp,
        'org_id': org_id,
        'project_id': project_id,
        'key_id': key_id,
        'outcome': outcome.value,
        'reason': reason,
        'event_id': event_id,
    }))
    metrics.incr('events.outcomes', skip_internal=True, tags={
        'outcome': outcome.name.lower(),
        'reason': reason,
    })