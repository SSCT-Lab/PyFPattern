

def request(self, path, method=None, payload=None):
    'Generic HTTP method for Meraki requests.'
    self.path = path
    self.define_protocol()
    if (method is not None):
        self.method = method
    self.url = '{protocol}://{host}/api/v0/{path}'.format(path=self.path.lstrip('/'), **self.params)
    (resp, info) = fetch_url(self.module, self.url, headers=self.headers, data=payload, method=self.method, timeout=self.params['timeout'], use_proxy=self.params['use_proxy'])
    self.response = info['msg']
    self.status = info['status']
    if (self.status >= 500):
        self.fail_json(msg='Request failed for {url}: {status} - {msg}'.format(**info))
    elif (self.status >= 300):
        self.fail_json(msg='Request failed for {url}: {status} - {msg}'.format(**info), body=json.loads(to_native(info['body'])))
    try:
        return json.loads(to_native(resp.read()))
    except:
        pass
