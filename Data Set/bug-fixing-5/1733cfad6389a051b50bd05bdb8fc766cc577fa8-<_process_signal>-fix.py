def _process_signal(msg):
    project_id = int((msg.get('project_id') or 0))
    if (project_id == 0):
        metrics.incr('outcomes_consumer.skip_outcome', tags={
            'reason': 'project_zero',
        })
        return
    outcome = int(msg.get('outcome', (- 1)))
    if (outcome not in (Outcome.FILTERED, Outcome.RATE_LIMITED)):
        metrics.incr('outcomes_consumer.skip_outcome', tags={
            'reason': 'wrong_outcome_type',
        })
        return
    event_id = msg.get('event_id')
    if (not event_id):
        return
    if is_signal_sent(project_id=project_id, event_id=event_id):
        metrics.incr('outcomes_consumer.skip_outcome', tags={
            'reason': 'is_signal_sent',
        })
        return
    try:
        project = Project.objects.get_from_cache(id=project_id)
    except Project.DoesNotExist:
        logger.error('OutcomesConsumer could not find project with id: %s', project_id)
        return
    reason = msg.get('reason')
    remote_addr = msg.get('remote_addr')
    if (outcome == Outcome.FILTERED):
        event_filtered.send_robust(ip=remote_addr, project=project, sender=OutcomesConsumerWorker)
    elif (outcome == Outcome.RATE_LIMITED):
        event_dropped.send_robust(ip=remote_addr, project=project, reason_code=reason, sender=OutcomesConsumerWorker)
    mark_signal_sent(project_id=project_id, event_id=event_id)
    timestamp = msg.get('timestamp')
    if (timestamp is not None):
        delta = (to_datetime(time.time()) - parse_timestamp(timestamp))
        metrics.timing('outcomes_consumer.timestamp_lag', delta.total_seconds())
    metrics.incr('outcomes_consumer.signal_sent', tags={
        'reason': reason,
        'outcome': outcome,
    })