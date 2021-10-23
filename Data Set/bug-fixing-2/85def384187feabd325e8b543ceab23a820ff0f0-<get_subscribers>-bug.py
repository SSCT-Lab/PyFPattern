

def get_subscribers(self, **request):
    "\n            Example usage: client.get_subscribers(stream='devel')\n        "
    request_stream_id = self.get_stream_id(request['stream'])
    try:
        stream_id = request_stream_id['stream_id']
    except KeyError:
        return request_stream_id
    url = ('streams/%d/members' % (stream_id,))
    return self.call_endpoint(url=url, method='GET', request=request)
