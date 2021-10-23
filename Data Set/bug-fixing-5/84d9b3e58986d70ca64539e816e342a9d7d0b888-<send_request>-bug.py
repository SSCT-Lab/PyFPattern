def send_request(self, data, **message_kwargs):
    data = to_list(data)
    if self._become:
        self.connection.queue_message('vvvv', 'firing event: on_become')
        data.insert(0, {
            'cmd': 'enable',
            'input': self._become_pass,
        })
    output = message_kwargs.get('output', 'text')
    request = request_builder(data, output)
    headers = {
        'Content-Type': 'application/json-rpc',
    }
    (response, response_data) = self.connection.send('/command-api', request, headers=headers, method='POST')
    try:
        response_data = json.loads(to_text(response_data.getvalue()))
    except ValueError:
        raise ConnectionError('Response was not valid JSON, got {0}'.format(to_text(response_data.getvalue())))
    results = handle_response(response_data)
    if self._become:
        results = results[1:]
    if (len(results) == 1):
        results = results[0]
    return results