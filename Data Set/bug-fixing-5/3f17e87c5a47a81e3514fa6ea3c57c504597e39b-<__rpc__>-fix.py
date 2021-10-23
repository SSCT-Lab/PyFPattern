def __rpc__(self, name, *args, **kwargs):
    'Executes the json-rpc and returns the output received\n           from remote device.\n           :name: rpc method to be executed over connection plugin that implements jsonrpc 2.0\n           :args: Ordered list of params passed as arguments to rpc method\n           :kwargs: Dict of valid key, value pairs passed as arguments to rpc method\n\n           For usage refer the respective connection plugin docs.\n        '
    req = request_builder(name, *args, **kwargs)
    reqid = req['id']
    if (not self._module._socket_path):
        self._module.fail_json(msg='provider support not available for this host')
    if (not os.path.exists(self._module._socket_path)):
        self._module.fail_json(msg='provider socket does not exist, is the provider running?')
    try:
        data = self._module.jsonify(req)
        (rc, out, err) = exec_command(self._module, data)
    except socket.error:
        exc = get_exception()
        self._module.fail_json(msg='unable to connect to socket', err=str(exc))
    try:
        response = self._module.from_json(to_text(out, errors='surrogate_then_replace'))
    except ValueError as exc:
        self._module.fail_json(msg=to_text(exc, errors='surrogate_then_replace'))
    if (response['id'] != reqid):
        self._module.fail_json(msg='invalid id received')
    if ('error' in response):
        msg = (response['error'].get('data') or response['error']['message'])
        self._module.fail_json(msg=to_text(msg, errors='surrogate_then_replace'))
    return response['result']