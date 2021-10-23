

def _forwards(self, orm):
    'Write your forwards methods here.'
    from sentry.utils.query import RangeQuerySetWrapperWithProgressBar
    GroupCommitResolution = orm['sentry.GroupCommitResolution']
    GroupLink = orm['sentry.GroupLink']
    Group = orm['sentry.Group']
    queryset = GroupCommitResolution.objects.all()
    for group_commit_resolution in RangeQuerySetWrapperWithProgressBar(queryset):
        try:
            project_id = Group.objects.filter(id=group_commit_resolution.group_id).values_list('project_id', flat=True)[0]
            with transaction.atomic():
                GroupLink.objects.create(group_id=group_commit_resolution.group_id, linked_id=group_commit_resolution.commit_id, datetime=group_commit_resolution.datetime, project_id=project_id, linked_type=1, relationship=1)
        except (IntegrityError, IndexError):
            pass
