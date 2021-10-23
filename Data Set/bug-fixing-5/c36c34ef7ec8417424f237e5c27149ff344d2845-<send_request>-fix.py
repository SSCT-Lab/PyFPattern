def send_request(self, commands, output='text', check_status=True):
    if (output != 'config'):
        commands = collections.deque(to_list(commands))
        stack = list()
        requests = list()
        while commands:
            stack.append(commands.popleft())
            if (len(stack) == 10):
                body = self._request_builder(stack, output)
                data = self._module.jsonify(body)
                requests.append(data)
                stack = list()
        if stack:
            body = self._request_builder(stack, output)
            data = self._module.jsonify(body)
            requests.append(data)
    else:
        body = self._request_builder(commands, 'config')
        requests = [self._module.jsonify(body)]
    headers = {
        'Content-Type': 'application/json',
    }
    result = list()
    timeout = self._module.params['timeout']
    for req in requests:
        if self._nxapi_auth:
            headers['Cookie'] = self._nxapi_auth
        (response, headers) = fetch_url(self._module, self._url, data=req, headers=headers, timeout=timeout, method='POST')
        self._nxapi_auth = headers.get('set-cookie')
        if (headers['status'] != 200):
            self._error(**headers)
        try:
            response = self._module.from_json(response.read())
        except ValueError:
            self._module.fail_json(msg='unable to parse response')
        if response['ins_api'].get('outputs'):
            output = response['ins_api']['outputs']['output']
            for item in to_list(output):
                if (check_status and (item['code'] != '200')):
                    self._error(output=output, **item)
                elif ('body' in item):
                    result.append(item['body'])
        return result