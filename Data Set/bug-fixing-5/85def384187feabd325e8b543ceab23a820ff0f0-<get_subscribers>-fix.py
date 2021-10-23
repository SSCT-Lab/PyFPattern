def get_subscribers(self, **request):
    "\n            Example usage: client.get_subscribers(stream='devel')\n        "
    response = self.get_stream_id(request['stream'])
    if (response['result'] == 'error'):
        return response
    stream_id = response['stream_id']
    url = ('streams/%d/members' % (stream_id,))
    return self.call_endpoint(url=url, method='GET', request=request)