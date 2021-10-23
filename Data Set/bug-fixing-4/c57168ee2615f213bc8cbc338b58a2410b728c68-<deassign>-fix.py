def deassign(self, group, acting_user=None):
    from sentry import features
    affected = GroupAssignee.objects.filter(group=group)[:1].count()
    GroupAssignee.objects.filter(group=group).delete()
    if (affected > 0):
        activity = Activity.objects.create(project=group.project, group=group, type=Activity.UNASSIGNED, user=acting_user)
        activity.send_notification()
        if features.has('organizations:internal-catchall', group.organization, actor=acting_user):
            sync_group_assignee(group, None, assign=False)