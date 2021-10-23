

def process_event(event_manager, project, key, remote_addr, helper, attachments, project_config):
    event_received.send_robust(ip=remote_addr, project=project, sender=process_event)
    start_time = time()
    data = event_manager.get_data()
    (should_filter, filter_reason) = event_manager.should_filter()
    del event_manager
    event_id = data['event_id']
    if should_filter:
        signals_in_consumer = decide_signals_in_consumer()
        if (not signals_in_consumer):
            mark_signal_sent(project_config.project_id, event_id)
        track_outcome(project_config.organization_id, project_config.project_id, key.id, Outcome.FILTERED, filter_reason, event_id=event_id)
        metrics.incr('events.blacklisted', tags={
            'reason': filter_reason,
        }, skip_internal=False)
        if (not signals_in_consumer):
            event_filtered.send_robust(ip=remote_addr, project=project, sender=process_event)
        raise APIForbidden(('Event dropped due to filter: %s' % (filter_reason,)))
    rate_limit = safe_execute(quotas.is_rate_limited, project=project, key=key, _with_transaction=False)
    if isinstance(rate_limit, bool):
        rate_limit = RateLimit(is_limited=rate_limit, retry_after=None)
    if ((rate_limit is None) or rate_limit.is_limited):
        if (rate_limit is None):
            api_logger.debug('Dropped event due to error with rate limiter')
        signals_in_consumer = decide_signals_in_consumer()
        if (not signals_in_consumer):
            mark_signal_sent(project_config.project_id, event_id)
        reason = (rate_limit.reason_code if rate_limit else None)
        track_outcome(project_config.organization_id, project_config.project_id, key.id, Outcome.RATE_LIMITED, reason, event_id=event_id)
        metrics.incr('events.dropped', tags={
            'reason': (reason or 'unknown'),
        }, skip_internal=False)
        if (not signals_in_consumer):
            event_dropped.send_robust(ip=remote_addr, project=project, reason_code=reason, sender=process_event)
        if (rate_limit is not None):
            raise APIRateLimited(rate_limit.retry_after)
    cache_key = ('ev:%s:%s' % (project_config.project_id, event_id))
    if (cache.get(cache_key) is not None):
        track_outcome(project_config.organization_id, project_config.project_id, key.id, Outcome.INVALID, 'duplicate', event_id=event_id)
        raise APIForbidden(('An event with the same ID already exists (%s)' % (event_id,)))
    config = project_config.config
    datascrubbing_settings = (config.get('datascrubbingSettings') or {
        
    })
    scrub_ip_address = datascrubbing_settings.get('scrubIpAddresses')
    scrub_data = datascrubbing_settings.get('scrubData')
    if (random.random() < options.get('store.sample-rust-data-scrubber', 0.0)):
        rust_scrubbed_data = safe_execute(semaphore.scrub_event, datascrubbing_settings, data, _with_transaction=False)
    else:
        rust_scrubbed_data = None
    if (rust_scrubbed_data and options.get('store.use-rust-data-scrubber', False)):
        data = rust_scrubbed_data
        data['_rust_data_scrubbed'] = True
    else:
        if scrub_data:
            sensitive_fields = datascrubbing_settings.get('sensitiveFields')
            exclude_fields = datascrubbing_settings.get('excludeFields')
            scrub_defaults = datascrubbing_settings.get('scrubDefaults')
            SensitiveDataFilter(fields=sensitive_fields, include_defaults=scrub_defaults, exclude_fields=exclude_fields).apply(data)
        if scrub_ip_address:
            helper.ensure_does_not_have_ip(data)
    helper.insert_data_to_database(data, start_time=start_time, attachments=attachments)
    cache.set(cache_key, '', (60 * 60))
    api_logger.debug('New event received (%s)', event_id)
    event_accepted.send_robust(ip=remote_addr, data=data, project=project, sender=process_event)
    return event_id
