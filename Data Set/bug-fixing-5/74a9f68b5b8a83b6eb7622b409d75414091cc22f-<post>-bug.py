def post(self, request, project):
    event = create_sample_event(project, platform=project.platform, default='javascript', level=0)
    data = serialize(event, request.user)
    return Response(data)