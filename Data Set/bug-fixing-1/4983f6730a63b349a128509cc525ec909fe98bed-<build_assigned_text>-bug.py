

def build_assigned_text(identity, assignee):
    if (assignee == 'none'):
        return '*Issue unassigned by <@{user_id}>*'.format(user_id=identity.external_id)
    try:
        assignee_user = User.objects.get(email=assignee)
    except User.DoesNotExist:
        return
    try:
        assignee_ident = Identity.objects.get(user=assignee_user)
        assignee_text = '<@{}>'.format(assignee_ident.external_id)
    except Identity.DoesNotExist:
        assignee_text = assignee_user.get_display_name()
    return '*Issue assigned to {assignee_text} by <@{user_id}>*'.format(assignee_text=assignee_text, user_id=identity.external_id)
