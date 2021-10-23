

def view_link(self, request, group, **kwargs):
    auth_errors = self.check_config_and_auth(request, group)
    if auth_errors:
        return Response(auth_errors, status=400)
    event = group.get_latest_event()
    Event.objects.bind_nodes([event], 'data')
    try:
        fields = self.get_link_existing_issue_fields(request, group, event, **kwargs)
    except Exception as e:
        return self.handle_api_error(e)
    if (request.method == 'GET'):
        return Response(fields)
    errors = self.validate_form(fields, request.DATA)
    if errors:
        return Response({
            'error_type': 'validation',
            'errors': errors,
        }, status=400)
    issue_id = int(request.DATA['issue_id'])
    try:
        issue = self.link_issue(group=group, form_data=request.DATA, request=request)
        if (issue is None):
            issue = {
                'title': self.get_issue_title_by_id(request, group, issue_id),
            }
    except Exception as e:
        return self.handle_api_error(e)
    GroupMeta.objects.set_value(group, ('%s:tid' % self.get_conf_key()), issue_id)
    issue_information = {
        'title': issue['title'],
        'provider': self.get_title(),
        'location': self.get_issue_url(group, issue_id),
        'label': self.get_issue_label(group=group, issue_id=issue_id),
    }
    Activity.objects.create(project=group.project, group=group, type=Activity.CREATE_ISSUE, user=request.user, data=issue_information)
    return Response({
        'message': 'Successfully linked issue.',
    })
