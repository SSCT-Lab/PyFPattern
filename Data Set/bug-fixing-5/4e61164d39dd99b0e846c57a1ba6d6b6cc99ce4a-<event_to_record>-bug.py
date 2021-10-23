def event_to_record(event, rules):
    if (not rules):
        logger.warning('Creating record for %r that does not contain any rules!', event)
    if options.get('store.use-django-event'):
        event_data = strip_for_serialization(event)
    else:
        event_data = event
    return Record(event.event_id, Notification(event_data, [rule.id for rule in rules]), to_timestamp(event.datetime))