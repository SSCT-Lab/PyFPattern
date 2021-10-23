

def _exec_jsonrpc(self, name, *args, **kwargs):
    req = request_builder(name, *args, **kwargs)
    reqid = req['id']
    troubleshoot = 'http://docs.ansible.com/ansible/latest/network/user_guide/network_debug_troubleshooting.html#category-socket-path-issue'
    if (not os.path.exists(self.socket_path)):
        raise ConnectionError(('socket_path does not exist or cannot be found. Please check %s' % troubleshoot))
    try:
        data = json.dumps(req)
        out = self.send(data)
        response = json.loads(out)
    except socket.error as e:
        raise ConnectionError(('unable to connect to socket. Please check %s' % troubleshoot), err=to_text(e, errors='surrogate_then_replace'), exception=traceback.format_exc())
    if (response['id'] != reqid):
        raise ConnectionError('invalid json-rpc id received')
    return response
