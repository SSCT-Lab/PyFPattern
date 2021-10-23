def _handle_builtin(self, request, project):
    endpoint = '/projects/{}/{}/releases/'.format(project.organization.slug, project.slug)
    try:
        data = json.loads(request.body)
    except JSONDecodeError as exc:
        return HttpResponse(status=400, content=json.dumps({
            'error': six.text_type(exc),
        }), content_type='application/json')
    try:
        god = ApiKey(organization=project.organization, scopes=getattr(ApiKey.scopes, 'project:write'))
        resp = client.post(endpoint, data=data, auth=god)
    except client.ApiError as exc:
        return HttpResponse(status=exc.status_code, content=exc.body, content_type='application/json')
    return HttpResponse(status=resp.status_code, content=json.dumps(resp.data), content_type='application/json')