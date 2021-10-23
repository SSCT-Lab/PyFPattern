

def fetch_personal_statistics(start__stop, organization, user):
    (start, stop) = start__stop
    resolved_issue_ids = set(Activity.objects.filter(project__organization_id=organization.id, user_id=user.id, type__in=(Activity.SET_RESOLVED, Activity.SET_RESOLVED_IN_RELEASE), datetime__gte=start, datetime__lt=stop, group__status=GroupStatus.RESOLVED).distinct().values_list('group_id', flat=True))
    return {
        'resolved': len(resolved_issue_ids),
        'users': tsdb.get_distinct_counts_union(tsdb.models.users_affected_by_group, resolved_issue_ids, start, stop, ((60 * 60) * 24)),
    }
