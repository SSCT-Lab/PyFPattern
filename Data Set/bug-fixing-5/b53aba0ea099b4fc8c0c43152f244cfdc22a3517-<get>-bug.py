@attach_scenarios([retrieve_aggregate_scenario])
def get(self, request, group):
    '\n        Retrieve an Issue\n        `````````````````\n\n        Return details on an individual issue. This returns the basic stats for\n        the issue (title, last seen, first seen), some overall numbers (number\n        of comments, user reports) as well as the summarized event data.\n\n        :pparam string issue_id: the ID of the issue to retrieve.\n        :auth: required\n        '
    activity = self._get_activity(request, group, num=100)
    seen_by = self._get_seen_by(request, group)
    first_release = group.get_first_release()
    if (first_release is not None):
        last_release = group.get_last_release()
    else:
        last_release = None
    action_list = self._get_actions(request, group)
    if first_release:
        first_release = self._get_release_info(request, group, first_release)
    if last_release:
        last_release = self._get_release_info(request, group, last_release)
    use_snuba = (request.GET.get('enable_snuba') == '1')
    environments = get_environments(request, group.project.organization)
    environment_ids = [e.id for e in environments]
    if use_snuba:
        data = serialize(group, request.user, GroupSerializerSnuba(environment_ids=environment_ids))
    else:
        if environments:
            environments = environments[:1]
            environment_ids = environment_ids[:1]
        data = serialize(group, request.user, GroupSerializer(environment_func=(lambda : (environments[0] if environments else None))))
    get_range = functools.partial(tsdb.get_range, environment_ids=environment_ids)
    tags = tagstore.get_group_tag_keys(group.project_id, group.id, environment_ids, limit=100)
    if (not environment_ids):
        user_reports = UserReport.objects.filter(group=group)
    else:
        user_reports = UserReport.objects.filter(group=group, environment_id__in=environment_ids)
    now = timezone.now()
    hourly_stats = tsdb.rollup(get_range(model=tsdb.models.group, keys=[group.id], end=now, start=(now - timedelta(days=1))), 3600)[group.id]
    daily_stats = tsdb.rollup(get_range(model=tsdb.models.group, keys=[group.id], end=now, start=(now - timedelta(days=30))), (3600 * 24))[group.id]
    participants = list(User.objects.filter(groupsubscription__is_active=True, groupsubscription__group=group))
    data.update({
        'firstRelease': first_release,
        'lastRelease': last_release,
        'activity': serialize(activity, request.user),
        'seenBy': seen_by,
        'participants': serialize(participants, request.user),
        'pluginActions': action_list,
        'pluginIssues': self._get_available_issue_plugins(request, group),
        'pluginContexts': self._get_context_plugins(request, group),
        'userReportCount': user_reports.count(),
        'tags': sorted(serialize(tags, request.user), key=(lambda x: x['name'])),
        'stats': {
            '24h': hourly_stats,
            '30d': daily_stats,
        },
    })
    if environments:
        try:
            current_release = GroupRelease.objects.filter(group_id=group.id, environment__in=[env.name for env in environments], release_id=ReleaseEnvironment.objects.filter(release_id__in=ReleaseProject.objects.filter(project_id=group.project_id).values_list('release_id', flat=True), organization_id=group.project.organization_id, environment_id__in=environment_ids).order_by('-first_seen').values_list('release_id', flat=True)[:1])[0]
        except IndexError:
            current_release = None
        data.update({
            'currentRelease': serialize(current_release, request.user, GroupReleaseWithStatsSerializer()),
        })
    return Response(data)