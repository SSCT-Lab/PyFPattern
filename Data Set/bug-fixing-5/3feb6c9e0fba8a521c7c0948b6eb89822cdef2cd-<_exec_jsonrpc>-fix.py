def _exec_jsonrpc(self, name, *args, **kwargs):
    req = request_builder(name, *args, **kwargs)
    reqid = req['id']
    if (not os.path.exists(self.socket_path)):
        raise ConnectionError('socket_path does not exist or cannot be found.\nSee the socket_path issue catergory in Network Debug and Troubleshooting Guide')
    try:
        data = json.dumps(req)
    except TypeError as exc:
        data = req.get('params')
        if isinstance(data, dict):
            data = data.get('var_options', {
                
            })
            for (key, value) in iteritems(data):
                try:
                    dummy = json.dumps(value)
                except TypeError:
                    raise ConnectionError(("Failed to encode some variables as JSON for communication with ansible-connection. Please open an issue and mention that the culprit is most likely '%s'" % key))
        raise ConnectionError(('Failed to encode some variables as JSON for communication with ansible-connection. The original exception was: %s' % to_text(exc)))
    try:
        out = self.send(data)
    except socket.error as e:
        raise ConnectionError('unable to connect to socket. See the socket_path issue catergory in Network Debug and Troubleshooting Guide', err=to_text(e, errors='surrogate_then_replace'), exception=traceback.format_exc())
    try:
        response = json.loads(out)
    except ValueError:
        params = (list(args) + ['{0}={1}'.format(k, v) for (k, v) in iteritems(kwargs)])
        params = ', '.join(params)
        raise ConnectionError("Unable to decode JSON from response to {0}({1}). Received '{2}'.".format(name, params, out))
    if (response['id'] != reqid):
        raise ConnectionError('invalid json-rpc id received')
    return response