def post(self, request, token, *args, **kwargs):
    try:
        integration = get_integration_from_token(token)
    except ValueError as err:
        logger.info('token-validation-error', extra={
            'token': token,
            'error': six.text_type(err),
        })
        return self.respond(status=400)
    data = request.DATA
    if (not data.get('changelog')):
        logger.info('missing-changelog', extra={
            'integration_id': integration.id,
            'data': data,
        })
        return self.respond()
    handle_assignee_change(integration, data)
    handle_status_change(integration, data)
    return self.respond()