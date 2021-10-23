def post(self, request):
    logging_data = {
        
    }
    try:
        data = request.DATA
    except (ValueError, TypeError):
        logger.error('slack.action.invalid-json', extra=logging_data, exc_info=True)
        return self.respond(status=400)
    try:
        data = json.loads(data['payload'])
    except (KeyError, IndexError, TypeError, ValueError):
        logger.error('slack.action.invalid-payload', extra=logging_data, exc_info=True)
        return self.respond(status=400)
    event_id = data.get('event_id')
    team_id = data.get('team', {
        
    }).get('id')
    channel_id = data.get('channel', {
        
    }).get('id')
    user_id = data.get('user', {
        
    }).get('id')
    callback_id = data.get('callback_id')
    logging_data.update({
        'slack_team_id': team_id,
        'slack_channel_id': channel_id,
        'slack_user_id': user_id,
        'slack_event_id': event_id,
        'slack_callback_id': callback_id,
    })
    token = data.get('token')
    if (token != options.get('slack.verification-token')):
        logger.error('slack.action.invalid-token', extra=logging_data)
        return self.respond(status=401)
    logger.info('slack.action', extra=logging_data)
    try:
        integration = Integration.objects.get(provider='slack', external_id=team_id)
    except Integration.DoesNotExist:
        logger.error('slack.action.invalid-team-id', extra=logging_data)
        return self.respond(status=403)
    logging_data['integration_id'] = integration.id
    callback_data = json.loads(callback_id)
    group_id = callback_data['issue']
    action_list = data.get('actions', [])
    try:
        group = Group.objects.select_related('project__organization').get(project__in=Project.objects.filter(organization__in=integration.organizations.all()), id=group_id)
    except Group.DoesNotExist:
        logger.error('slack.action.invalid-issue', extra=logging_data)
        return self.respond(status=403)
    try:
        identity = Identity.objects.get(external_id=user_id, idp__organization=group.organization)
    except Identity.DoesNotExist:
        associate_url = build_linking_url(integration, group.organization, user_id, channel_id)
        return self.respond({
            'response_type': 'ephemeral',
            'replace_original': False,
            'text': LINK_IDENTITY_MESSAGE.format(associate_url=associate_url),
        })
    if ((data['type'] == 'dialog_submission') and ('resolve_type' in data['submission'])):
        action = {
            'name': 'status',
            'value': data['submission']['resolve_type'],
        }
        self.on_status(request, identity, group, action, data, integration)
        group = Group.objects.get(id=group.id)
        attachment = build_attachment(group, identity=identity, actions=[action])
        body = self.construct_reply(attachment, is_message=callback_data['is_message'])
        session = http.build_session()
        req = session.post(callback_data['orig_response_url'], json=body)
        resp = req.json()
        if (not resp.get('ok')):
            logger.error('slack.action.response-error', extra={
                'error': resp.get('error'),
            })
        return self.respond()
    defer_attachment_update = False
    try:
        for action in action_list:
            action_type = action['name']
            if (action_type == 'status'):
                self.on_status(request, identity, group, action, data, integration)
            elif (action_type == 'assign'):
                self.on_assign(request, identity, group, action)
            elif (action_type == 'resolve_dialog'):
                self.open_resolve_dialog(data, group, integration)
                defer_attachment_update = True
    except client.ApiError as e:
        return self.respond({
            'response_type': 'ephemeral',
            'replace_original': False,
            'text': 'Action failed: {}'.format(e.body['detail']),
        })
    if defer_attachment_update:
        return self.respond()
    group = Group.objects.get(id=group.id)
    attachment = build_attachment(group, identity=identity, actions=action_list)
    body = self.construct_reply(attachment, is_message=self.is_message(data))
    return self.respond(body)