

def post(self, request, project):
    event = create_sample_event(project, platform=project.platform, default='javascript')
    data = serialize(event, request.user)
    return Response(data)
