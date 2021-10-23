def assign(self, group, assigned_to, acting_user=None):
    from sentry import features
    from sentry.models import User, Team, GroupSubscription, GroupSubscriptionReason
    GroupSubscription.objects.subscribe_actor(group=group, actor=assigned_to, reason=GroupSubscriptionReason.assigned)
    if isinstance(assigned_to, User):
        assignee_type = 'user'
        other_type = 'team'
    elif isinstance(assigned_to, Team):
        assignee_type = 'team'
        other_type = 'user'
    else:
        raise AssertionError(('Invalid type to assign to: %r' % type(assigned_to)))
    now = timezone.now()
    (assignee, created) = GroupAssignee.objects.get_or_create(group=group, defaults={
        'project': group.project,
        assignee_type: assigned_to,
        'date_added': now,
    })
    if (not created):
        affected = GroupAssignee.objects.filter(group=group).exclude(**{
            assignee_type: assigned_to,
        }).update(**{
            assignee_type: assigned_to,
            other_type: None,
            'date_added': now,
        })
    else:
        affected = True
        issue_assigned.send(project=group.project, group=group, sender=acting_user)
    if affected:
        activity = Activity.objects.create(project=group.project, group=group, type=Activity.ASSIGNED, user=acting_user, data={
            'assignee': six.text_type(assigned_to.id),
            'assigneeEmail': getattr(assigned_to, 'email', None),
            'assigneeType': assignee_type,
        })
        activity.send_notification()
    if ((assignee_type == 'user') and features.has('organizations:internal-catchall', group.organization, actor=acting_user)):
        sync_group_assignee(group, assigned_to.id, assign=True)