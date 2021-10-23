def post(self, request, *args, **kwargs):
    data = request.DATA
    if (data['eventType'] == 'workitem.updated'):
        integration = Integration.objects.get(provider='vsts', external_id=data['resourceContainers']['collection']['id'])
        try:
            self.check_webhook_secret(request, integration)
        except AssertionError:
            return self.respond(status=401)
        self.handle_updated_workitem(data, integration)
    return self.respond()