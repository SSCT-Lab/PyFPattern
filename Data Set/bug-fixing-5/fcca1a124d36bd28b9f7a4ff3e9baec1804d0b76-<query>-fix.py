def query(self, path):
    ' Perform a query with no payload '
    self.path = path
    if (('port' in self.params) and (self.params['port'] is not None)):
        self.url = (('%(protocol)s://%(host)s:%(port)s/' % self.params) + path.lstrip('/'))
    else:
        self.url = (('%(protocol)s://%(host)s/' % self.params) + path.lstrip('/'))
    if self.params['private_key']:
        self.cert_auth(path=path, method='GET')
    (resp, query) = fetch_url(self.module, self.url, data=None, headers=self.headers, method='GET', timeout=self.params['timeout'], use_proxy=self.params['use_proxy'])
    if (query['status'] != 200):
        self.response = query['msg']
        self.status = query['status']
        try:
            self.response_json(query['body'])
            self.fail_json(msg=('APIC Error %(code)s: %(text)s' % self.error))
        except KeyError:
            self.fail_json(msg=('Connection failed for %(url)s. %(msg)s' % query))
    query = json.loads(resp.read())
    return (json.dumps(query['imdata'], sort_keys=True, indent=2) + '\n')