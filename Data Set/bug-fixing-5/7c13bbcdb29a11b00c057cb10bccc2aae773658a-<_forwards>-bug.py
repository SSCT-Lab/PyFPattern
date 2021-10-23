def _forwards(self, orm):
    'Write your forwards methods here.'
    from sentry.utils.query import RangeQuerySetWrapperWithProgressBar
    GroupCommitResolution = orm['sentry.GroupCommitResolution']
    GroupLink = orm['sentry.GroupLink']
    Group = orm['sentry.Group']
    queryset = GroupCommitResolution.objects.all()
    group_to_project_ids = dict(Group.objects.filter(id__in=queryset.values_list('group_id', flat=True)).values_list('id', 'project_id'))
    for group_commit_resolution in RangeQuerySetWrapperWithProgressBar(queryset):
        try:
            with transaction.atomic():
                GroupLink.objects.create(group_id=group_commit_resolution.group_id, linked_id=group_commit_resolution.commit_id, datetime=group_commit_resolution.datetime, project_id=group_to_project_ids[group_commit_resolution.group_id], linked_type=1, relationship=1)
        except IntegrityError:
            pass