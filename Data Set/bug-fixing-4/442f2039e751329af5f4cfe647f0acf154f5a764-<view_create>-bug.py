def view_create(self, request, group, **kwargs):
    auth_errors = self.check_config_and_auth(request, group)
    if auth_errors:
        return Response(auth_errors, status=400)
    event = group.get_latest_event()
    Event.objects.bind_nodes([event], 'data')
    try:
        fields = self.get_new_issue_fields(request, group, event, **kwargs)
    except PluginError as e:
        return Response({
            'error_type': 'validation',
            'errors': {
                '__all__': e.message,
            },
        }, status=400)
    if (request.method == 'GET'):
        return Response(fields)
    errors = self.validate_form(fields, request.DATA)
    if errors:
        return Response({
            'error_type': 'validation',
            'errors': errors,
        }, status=400)
    try:
        issue_id = self.create_issue(group=group, form_data=request.DATA, request=request)
    except InvalidIdentity as e:
        return Response({
            'error_type': 'auth',
            'auth_url': reverse('socialauth_associate', args=[self.auth_provider]),
        })
    except PluginError as e:
        return Response({
            'error_type': 'validation',
            'errors': {
                '__all__': e.message,
            },
        }, status=400)
    GroupMeta.objects.set_value(group, ('%s:tid' % self.get_conf_key()), issue_id)
    issue_information = {
        'title': request.DATA['title'],
        'provider': self.get_title(),
        'location': self.get_issue_url(group, issue_id),
        'label': self.get_issue_label(group=group, issue_id=issue_id),
    }
    Activity.objects.create(project=group.project, group=group, type=Activity.CREATE_ISSUE, user=request.user, data=issue_information)
    issue_tracker_used.send(plugin=self, project=group.project, user=request.user, sender=IssueTrackingPlugin2)
    return Response({
        'issue_url': self.get_issue_url(group=group, issue_id=issue_id),
    })