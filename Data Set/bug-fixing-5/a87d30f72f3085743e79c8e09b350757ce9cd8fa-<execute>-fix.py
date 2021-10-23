def execute(self, commands, output='json', **kwargs):
    'Send commands to the device.\n        '
    if (self.url is None):
        raise NetworkError('Not connected to endpoint.')
    if (self.enable is not None):
        commands.insert(0, self.enable)
    body = self._get_body(commands, output)
    data = json.dumps(body)
    headers = {
        'Content-Type': 'application/json-rpc',
    }
    timeout = self.url_args.params['timeout']
    (response, headers) = fetch_url(self.url_args, self.url, data=data, headers=headers, method='POST', timeout=timeout)
    if (headers['status'] != 200):
        raise NetworkError(**headers)
    try:
        response = json.loads(response.read())
    except ValueError:
        raise NetworkError('unable to load response from device')
    if ('error' in response):
        err = response['error']
        raise NetworkError(msg=err['message'], code=err['code'], data=err['data'], commands=commands)
    if self.enable:
        response['result'].pop(0)
    return response['result']