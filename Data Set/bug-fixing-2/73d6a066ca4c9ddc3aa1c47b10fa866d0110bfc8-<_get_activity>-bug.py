

def _get_activity(self, request, group, num):
    activity_items = set()
    activity = []
    activity_qs = Activity.objects.filter(group=group).order_by('-datetime').select_related('user')
    for item in activity_qs[:(num * 2)]:
        sig = (item.type, item.ident, item.user_id, hash(frozenset(item.data.items())))
        if (item.type == Activity.NOTE):
            activity.append(item)
        elif (sig not in activity_items):
            activity_items.add(sig)
            activity.append(item)
    activity.append(Activity(id=0, project=group.project, group=group, type=Activity.FIRST_SEEN, datetime=group.first_seen))
    return activity[:num]
