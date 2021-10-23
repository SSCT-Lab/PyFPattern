def build_attachment(group, event=None, tags=None, identity=None, actions=None, rules=None):
    status = group.get_status()
    members = get_member_assignees(group)
    teams = get_team_assignees(group)
    logo_url = absolute_uri(get_asset_url('sentry', 'images/sentry-email-avatar.png'))
    color = NEW_ISSUE_COLOR
    text = (build_attachment_text(group, event) or '')
    if (actions is None):
        actions = []
    assignee = get_assignee(group)
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
    option_groups = []
    if teams:
        option_groups.append({
            'text': 'Teams',
            'options': teams,
        })
    if members:
        option_groups.append({
            'text': 'People',
            'options': members,
        })
    payload_actions = [resolve_button, ignore_button, {
        'name': 'assign',
        'text': 'Select Assignee...',
        'type': 'select',
        'selected_options': [assignee],
        'option_groups': option_groups,
    }]
    if (not features.has('organizations:new-teams', group.organization)):
        payload_actions[2]['options'] = members
        del payload_actions[2]['option_groups']
    fields = []
    if tags:
        event_tags = (event.tags if event else group.get_latest_event().tags)
        for (key, value) in event_tags:
            std_key = tagstore.get_standardized_key(key)
            if (std_key not in tags):
                continue
            labeled_value = tagstore.get_tag_value_label(key, value)
            fields.append({
                'title': std_key.encode('utf-8'),
                'value': labeled_value.encode('utf-8'),
                'short': True,
            })
    if actions:
        action_texts = filter(None, [build_action_text(group, identity, a) for a in actions])
        text += ('\n' + '\n'.join(action_texts))
        color = ACTIONED_ISSUE_COLOR
        payload_actions = []
    ts = group.last_seen
    if event:
        event_ts = event.datetime
        ts = max(ts, event_ts)
    footer = '{}'.format(group.qualified_short_id)
    if rules:
        footer += ' via {}'.format(rules[0].label)
        if (len(rules) > 1):
            footer += ' (+{} other)'.format((len(rules) - 1))
    return {
        'fallback': '[{}] {}'.format(group.project.slug, group.title),
        'title': build_attachment_title(group, event),
        'title_link': add_notification_referrer_param(group.get_absolute_url(), 'slack'),
        'text': text,
        'fields': fields,
        'mrkdwn_in': ['text'],
        'callback_id': json.dumps({
            'issue': group.id,
        }),
        'footer_icon': logo_url,
        'footer': footer,
        'ts': to_timestamp(ts),
        'color': color,
        'actions': payload_actions,
    }