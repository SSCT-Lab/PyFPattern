

def send_request(self, commands, output='text'):
    commands = to_list(commands)
    if self._enable:
        commands.insert(0, 'enable')
    body = self._request_builder(commands, output)
    data = self._module.jsonify(body)
    headers = {
        'Content-Type': 'application/json-rpc',
    }
    timeout = self._module.params['timeout']
    (response, headers) = fetch_url(self._module, self._url, data=data, headers=headers, method='POST', timeout=timeout)
    if (headers['status'] != 200):
        self._module.fail_json(**headers)
    try:
        data = response.read()
        response = self._module.from_json(to_text(data, errors='surrogate_then_replace'))
    except ValueError:
        self._module.fail_json(msg='unable to load response from device', data=data)
    if (self._enable and ('result' in response)):
        response['result'].pop(0)
    return response
