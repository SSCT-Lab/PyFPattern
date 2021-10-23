

def build_attachment(group, event=None, identity=None, actions=None):
    status = group.get_status()
    assignees = get_assignees(group)
    logo_url = absolute_uri(get_asset_url('sentry', 'images/sentry-email-avatar.png'))
    color = NEW_ISSUE_COLOR
    text = (build_attachment_text(group, event) or '')
    if (actions is None):
        actions = []
    try:
        assignee = GroupAssignee.objects.get(group=group).user
        assignee = {
            'text': assignee.get_display_name(),
            'value': assignee.username,
        }
        assignees.insert(0, UNASSIGN_OPTION)
    except GroupAssignee.DoesNotExist:
        assignee = None
    resolve_button = {
        'name': 'resolve_dialog',
        'value': 'resolve_dialog',
        'type': 'button',
        'text': 'Resolve...',
    }
    ignore_button = {
        'name': 'status',
        'value': 'ignored',
        'type': 'button',
        'text': 'Ignore',
    }
    if (status == GroupStatus.RESOLVED):
        resolve_button.update({
            'name': 'status',
            'text': 'Unresolve',
            'value': 'unresolved',
        })
    if (status == GroupStatus.IGNORED):
        ignore_button.update({
            'text': 'Stop Ignoring',
            'value': 'unresolved',
        })
    payload_actions = [resolve_button, ignore_button, {
        'name': 'assign',
        'text': 'Select Assignee ..',
        'type': 'select',
        'options': assignees,
        'selected_options': [assignee],
    }]
    if actions:
        action_texts = filter(None, [build_action_text(identity, a) for a in actions])
        text += ('\n' + '\n'.join(action_texts))
        color = ACTIONED_ISSUE_COLOR
        payload_actions = []
    return {
        'fallback': '[{}] {}'.format(group.project.slug, group.title),
        'title': build_attachment_title(group, event),
        'title_link': add_notification_referrer_param(group.get_absolute_url(), 'slack'),
        'text': text,
        'mrkdwn_in': ['text'],
        'callback_id': json.dumps({
            'issue': group.id,
        }),
        'footer_icon': logo_url,
        'footer': '{} / {}'.format(group.organization.slug, group.project.slug),
        'ts': int(time.mktime(group.last_seen.timetuple())),
        'color': color,
        'actions': payload_actions,
    }
