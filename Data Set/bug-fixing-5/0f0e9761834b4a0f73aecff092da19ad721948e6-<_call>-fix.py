def _call(self, payload):
    self._id += 1
    if ('id' not in payload):
        payload['id'] = self._id
    if ('jsonrpc' not in payload):
        payload['jsonrpc'] = '2.0'
    data = json.dumps(payload)
    resp = open_url(self._url, timeout=self._timeout, method='POST', data=data, headers=self._headers)
    if (resp.code != 200):
        raise NsoException('NSO returned HTTP code {0}, expected 200'.format(resp.status), {
            
        })
    resp_body = to_text(resp.read())
    resp_json = json.loads(resp_body)
    if ('error' in resp_json):
        self._handle_call_error(payload, resp_json)
    return (resp, resp_json)