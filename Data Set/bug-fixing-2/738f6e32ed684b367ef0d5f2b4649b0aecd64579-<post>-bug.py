

def post(self, request):
    try:
        slack_request = SlackEventRequest(request)
        slack_request.validate()
    except SlackRequestError as e:
        return self.respond(status=e.status)
    if slack_request.is_challenge():
        return self.on_url_verification(request, slack_request.data)
    if (slack_request.type == 'link_shared'):
        return self.on_link_shared(request, slack_request.integration, slack_request.data.get('token'), slack_request.data.get('event'))
    return self.respond()
