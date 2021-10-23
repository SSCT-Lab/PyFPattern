def query(self, project, tags=None, environment=None, sort_by='date', limit=100, cursor=None, count_hits=False, paginator_options=None, **parameters):
    from sentry.models import Group, GroupAssignee, GroupStatus, GroupSubscription, Release
    if (paginator_options is None):
        paginator_options = {
            
        }
    if (tags is None):
        tags = {
            
        }
    try:
        if (tags.get('sentry:release') == 'latest'):
            tags['sentry:release'] = get_latest_release(project, environment)
        if (parameters.get('first_release') == 'latest'):
            parameters['first_release'] = get_latest_release(project, environment)
    except Release.DoesNotExist:
        return Paginator(Group.objects.none()).get_result()
    group_queryset = QuerySetBuilder({
        'query': CallbackCondition((lambda queryset, query: (queryset.filter((Q(message__icontains=query) | Q(culprit__icontains=query))) if query else queryset))),
        'status': CallbackCondition((lambda queryset, status: queryset.filter(status=status))),
        'bookmarked_by': CallbackCondition((lambda queryset, user: queryset.filter(bookmark_set__project=project, bookmark_set__user=user))),
        'assigned_to': CallbackCondition(functools.partial(assigned_to_filter, project=project)),
        'unassigned': CallbackCondition((lambda queryset, unassigned: (queryset.exclude if unassigned else queryset.filter)(id__in=GroupAssignee.objects.filter(project_id=project.id).values_list('group_id', flat=True)))),
        'subscribed_by': CallbackCondition((lambda queryset, user: queryset.filter(id__in=GroupSubscription.objects.filter(project=project, user=user, is_active=True).values_list('group')))),
        'active_at_from': ScalarCondition('active_at', 'gt'),
        'active_at_to': ScalarCondition('active_at', 'lt'),
    }).build(Group.objects.filter(project=project).exclude(status__in=[GroupStatus.PENDING_DELETION, GroupStatus.DELETION_IN_PROGRESS, GroupStatus.PENDING_MERGE]), parameters)
    retention = quotas.get_event_retention(organization=project.organization)
    if retention:
        retention_window_start = (timezone.now() - timedelta(days=retention))
    else:
        retention_window_start = None
    if retention_window_start:
        group_queryset = group_queryset.filter(last_seen__gte=retention_window_start)
    return self._query(project, retention_window_start, group_queryset, tags, environment, sort_by, limit, cursor, count_hits, paginator_options, **parameters)