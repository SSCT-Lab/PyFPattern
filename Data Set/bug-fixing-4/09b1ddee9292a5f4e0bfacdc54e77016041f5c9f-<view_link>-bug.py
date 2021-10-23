def view_link(self, request, group, **kwargs):
    auth_errors = self.check_config_and_auth(request, group)
    if auth_errors:
        return Response(auth_errors, status=400)
    event = group.get_latest_event()
    Event.objects.bind_nodes([event], 'data')
    fields = self.get_link_existing_issue_fields(request, group, event, **kwargs)
    if (request.method == 'GET'):
        return Response(fields)
    errors = self.validate_form(fields, request.DATA)
    if errors:
        return Response({
            'error_type': 'validation',
            'errors': errors,
        }, status=400)
    try:
        self.link_issue(group=group, form_data=request.DATA, request=request)
    except PluginError as e:
        return Response({
            'error_type': 'validation',
            'errors': [{
                '__all__': e.message,
            }],
        }, status=400)
    issue_id = int(request.DATA['issue_id'])
    GroupMeta.objects.set_value(group, ('%s:tid' % self.get_conf_key()), issue_id)
    issue_information = {
        'title': self.get_issue_title_by_id(request, group, issue_id),
        'provider': self.get_title(),
        'location': self.get_issue_url(group, issue_id),
        'label': self.get_issue_label(group=group, issue_id=issue_id),
    }
    Activity.objects.create(project=group.project, group=group, type=Activity.CREATE_ISSUE, user=request.user, data=issue_information)
    return Response({
        'message': 'Successfully linked issue.',
    })