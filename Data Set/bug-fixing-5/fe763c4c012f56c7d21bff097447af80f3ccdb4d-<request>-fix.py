def request(self, method, path, headers=None, data=None, api_key=None, format='json'):
    if (api_key is None):
        api_key = self.api_key
    path = ('/api/0/' + path.lstrip('/'))
    headers = dict((headers or {
        
    }))
    request_is_json = True
    body = None
    files = None
    was_multipart = False
    if (data is not None):
        if (format == 'json'):
            body = json.dumps(data, sort_keys=True)
            headers['Content-Type'] = 'application/json'
        elif (format == 'multipart'):
            files = {
                
            }
            for (key, value) in data.items():
                if (hasattr(value, 'read') or isinstance(value, tuple)):
                    files[key] = value
                    del data[key]
                    was_multipart = True
            body = data
    req_headers = dict(headers)
    req_headers['Host'] = 'sentry.io'
    req_headers['Authorization'] = ('Bearer %s' % api_key.key.encode('utf-8'))
    url = ('http://127.0.0.1:%s%s' % (settings.SENTRY_APIDOCS_WEB_PORT, path))
    response = requests.request(method=method, url=url, files=files, headers=req_headers, data=body)
    response_headers = dict(response.headers)
    response_headers.pop('server', None)
    response_headers.pop('date', None)
    if (response.headers.get('Content-Type') == 'application/json'):
        response_data = response.json()
        is_json = True
    else:
        response_data = response.text
        is_json = False
    if was_multipart:
        headers['Content-Type'] = response.request.headers['content-type']
        data = response.request.body
        request_is_json = False
    rv = {
        'request': {
            'method': method,
            'path': path,
            'headers': headers,
            'data': data,
            'is_json': request_is_json,
        },
        'response': {
            'headers': response_headers,
            'status': response.status_code,
            'reason': response.reason,
            'data': response_data,
            'is_json': is_json,
        },
    }
    self.requests.append(rv)
    return rv