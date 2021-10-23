def update_group_status(self, groups, status, activity_type):
    updated = Group.objects.filter(id__in=[g.id for g in groups]).exclude(status=status).update(status=status)
    if updated:
        for group in groups:
            activity = Activity.objects.create(project=group.project, group=group, type=activity_type)
            activity.send_notification()