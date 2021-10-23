def track_outcome(org_id, project_id, key_id, outcome, reason=None, timestamp=None, event_id=None):
    '\n    This is a central point to track org/project counters per incoming event.\n    NB: This should only ever be called once per incoming event, which means\n    it should only be called at the point we know the final outcome for the\n    event (invalid, rate_limited, accepted, discarded, etc.)\n\n    This increments all the relevant legacy RedisTSDB counters, as well as\n    sending a single metric event to Kafka which can be used to reconstruct the\n    counters with SnubaTSDB.\n    '
    global outcomes_publisher
    if (outcomes_publisher is None):
        outcomes_publisher = QueuedPublisherService(KafkaPublisher(settings.KAFKA_CLUSTERS[outcomes['cluster']]))
    assert isinstance(org_id, six.integer_types)
    assert isinstance(project_id, six.integer_types)
    assert isinstance(key_id, (type(None), six.integer_types))
    assert isinstance(outcome, Outcome)
    assert isinstance(timestamp, (type(None), datetime))
    timestamp = (timestamp or to_datetime(time.time()))
    increment_list = []
    if (outcome != Outcome.INVALID):
        increment_list.extend([(tsdb.models.project_total_received, project_id), (tsdb.models.organization_total_received, org_id), (tsdb.models.key_total_received, key_id)])
    if (outcome == Outcome.FILTERED):
        increment_list.extend([(tsdb.models.project_total_blacklisted, project_id), (tsdb.models.organization_total_blacklisted, org_id), (tsdb.models.key_total_blacklisted, key_id)])
    elif (outcome == Outcome.RATE_LIMITED):
        increment_list.extend([(tsdb.models.project_total_rejected, project_id), (tsdb.models.organization_total_rejected, org_id), (tsdb.models.key_total_rejected, key_id)])
    if (reason in FILTER_STAT_KEYS_TO_VALUES):
        increment_list.append((FILTER_STAT_KEYS_TO_VALUES[reason], project_id))
    increment_list = [(model, key) for (model, key) in increment_list if (key is not None)]
    if increment_list:
        tsdb.incr_multi(increment_list, timestamp=timestamp)
    if (random.random() <= options.get('snuba.track-outcomes-sample-rate')):
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