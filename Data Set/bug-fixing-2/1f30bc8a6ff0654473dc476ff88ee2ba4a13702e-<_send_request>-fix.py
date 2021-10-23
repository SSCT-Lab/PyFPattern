

def _send_request(self, method, url, body_json=None, ok_error_codes=None, timeout=None):
    try:
        body = json.dumps(body_json)
        self.connection.request(method, url, body=body)
        resp = self.connection.getresponse()
        resp_json = json.loads(resp.read())
        self.logs.append({
            'type': 'sent request',
            'request': {
                'method': method,
                'url': url,
                'json': body_json,
                'timeout': timeout,
            },
            'response': {
                'json': resp_json,
            },
        })
        resp_type = resp_json.get('type', None)
        if (resp_type == 'error'):
            if ((ok_error_codes is not None) and (resp_json['error_code'] in ok_error_codes)):
                return resp_json
            if (resp_json['error'] == 'Certificate already in trust store'):
                return resp_json
            self._raise_err_from_json(resp_json)
        return resp_json
    except socket.error as e:
        raise LXDClientException('cannot connect to the LXD server', err=e)
