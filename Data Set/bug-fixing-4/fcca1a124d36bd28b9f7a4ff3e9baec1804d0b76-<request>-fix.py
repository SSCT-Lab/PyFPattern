def request(self, path, payload=None):
    ' Perform a REST request '
    self.define_method()
    self.path = path
    if (('port' in self.params) and (self.params['port'] is not None)):
        self.url = (('%(protocol)s://%(host)s:%(port)s/' % self.params) + path.lstrip('/'))
    else:
        self.url = (('%(protocol)s://%(host)s/' % self.params) + path.lstrip('/'))
    if self.params['private_key']:
        self.cert_auth(path=path, payload=payload)
    (resp, info) = fetch_url(self.module, self.url, data=payload, headers=self.headers, method=self.params['method'].upper(), timeout=self.params['timeout'], use_proxy=self.params['use_proxy'])
    self.response = info['msg']
    self.status = info['status']
    if (info['status'] != 200):
        try:
            self.response_json(info['body'])
            self.fail_json(msg=('APIC Error %(code)s: %(text)s' % self.error))
        except KeyError:
            self.fail_json(msg=('Connection failed for %(url)s. %(msg)s' % info))
    self.response_json(resp.read())