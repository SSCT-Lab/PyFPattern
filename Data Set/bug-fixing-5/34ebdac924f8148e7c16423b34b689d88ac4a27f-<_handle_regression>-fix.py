def _handle_regression(self, group, event, release):
    if (not group.is_resolved()):
        return
    elif GroupResolution.has_resolution(group, release):
        return
    if (not plugin_is_regression(group, event)):
        return
    date = max(event.datetime, group.last_seen)
    is_regression = bool(Group.objects.filter(id=group.id, status__in=[GroupStatus.RESOLVED, GroupStatus.UNRESOLVED]).exclude(active_at__gte=(date - timedelta(seconds=5))).update(active_at=date, last_seen=date, status=GroupStatus.UNRESOLVED))
    group.active_at = date
    group.status = GroupStatus.UNRESOLVED
    if (is_regression and release):
        try:
            resolution = GroupResolution.objects.get(group=group)
        except GroupResolution.DoesNotExist:
            affected = False
        else:
            cursor = connection.cursor()
            cursor.execute('DELETE FROM sentry_groupresolution WHERE id = %s', [resolution.id])
            affected = (cursor.rowcount > 0)
        if affected:
            try:
                activity = Activity.objects.filter(group=group, type=Activity.SET_RESOLVED_IN_RELEASE, ident=resolution.id).order_by('-datetime')[0]
            except IndexError:
                pass
            else:
                activity.update(data={
                    'version': release.version,
                })
    if is_regression:
        activity = Activity.objects.create(project=group.project, group=group, type=Activity.SET_REGRESSION, data={
            'version': (release.version if release else ''),
        })
        activity.send_notification()
        kick_off_status_syncs.apply_async(kwargs={
            'project_id': group.project_id,
            'group_id': group.id,
        })
    return is_regression