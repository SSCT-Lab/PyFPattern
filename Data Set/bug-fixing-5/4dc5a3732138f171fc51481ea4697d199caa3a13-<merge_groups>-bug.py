@instrumented_task(name='sentry.tasks.merge.merge_groups', queue='merge', default_retry_delay=(60 * 5), max_retries=None)
def merge_groups(from_object_ids=None, to_object_id=None, transaction_id=None, recursed=False, eventstream_state=None, **kwargs):
    from sentry.models import Activity, Group, GroupAssignee, GroupEnvironment, GroupHash, GroupRuleStatus, GroupSubscription, Environment, Event, EventAttachment, UserReport, GroupRedirect, GroupMeta, get_group_with_redirect
    if (not (from_object_ids and to_object_id)):
        logger.error('group.malformed.missing_params', extra={
            'transaction_id': transaction_id,
        })
        return
    from_object_id = from_object_ids[0]
    try:
        (new_group, _) = get_group_with_redirect(to_object_id)
    except Group.DoesNotExist:
        logger.warn('group.malformed.invalid_id', extra={
            'transaction_id': transaction_id,
            'old_object_ids': from_object_ids,
        })
        return
    if (not recursed):
        logger.info('merge.queued', extra={
            'transaction_id': transaction_id,
            'new_group_id': new_group.id,
            'old_group_ids': from_object_ids,
        })
    try:
        group = Group.objects.select_related('project').get(id=from_object_id)
    except Group.DoesNotExist:
        from_object_ids.remove(from_object_id)
        logger.warn('group.malformed.invalid_id', extra={
            'transaction_id': transaction_id,
            'old_object_id': from_object_id,
        })
    else:
        model_list = (tuple(EXTRA_MERGE_MODELS) + (Activity, GroupAssignee, GroupEnvironment, GroupHash, GroupRuleStatus, GroupSubscription, Event, EventAttachment, UserReport, GroupRedirect, GroupMeta))
        has_more = merge_objects(model_list, group, new_group, logger=logger, transaction_id=transaction_id)
        if (not has_more):
            from_object_ids.remove(from_object_id)
            features.merge(new_group, [group], allow_unsafe=True)
            environment_ids = list(Environment.objects.filter(projects=group.project).values_list('id', flat=True))
            for model in [tsdb.models.group]:
                tsdb.merge(model, new_group.id, [group.id], environment_ids=(environment_ids if (model in tsdb.models_with_environment_support) else None))
            for model in [tsdb.models.users_affected_by_group]:
                tsdb.merge_distinct_counts(model, new_group.id, [group.id], environment_ids=(environment_ids if (model in tsdb.models_with_environment_support) else None))
            for model in [tsdb.models.frequent_releases_by_group, tsdb.models.frequent_environments_by_group]:
                tsdb.merge_frequencies(model, new_group.id, [group.id], environment_ids=(environment_ids if (model in tsdb.models_with_environment_support) else None))
            previous_group_id = group.id
            with transaction.atomic():
                GroupRedirect.create_for_group(group, new_group)
                group.delete()
            delete_logger.info('object.delete.executed', extra={
                'object_id': previous_group_id,
                'transaction_id': transaction_id,
                'model': Group.__name__,
            })
            new_group.update(first_seen=min(group.first_seen, new_group.first_seen), last_seen=max(group.last_seen, new_group.last_seen))
            try:
                new_group.update(times_seen=(F('times_seen') + group.times_seen), num_comments=(F('num_comments') + group.num_comments))
            except DataError:
                pass
    if from_object_ids:
        merge_groups.delay(from_object_ids=from_object_ids, to_object_id=to_object_id, transaction_id=transaction_id, recursed=True, eventstream_state=eventstream_state)
        return
    if eventstream_state:
        eventstream.end_merge(eventstream_state)