

def query(self, path):
    ' Perform a query with no payload '
    url = (('%(protocol)s://%(hostname)s/' % self.params) + path.lstrip('/'))
    (resp, query) = fetch_url(self.module, url=url, data=None, method='GET', timeout=self.params['timeout'], headers=self.headers)
    if (query['status'] != 200):
        self.result['response'] = query['msg']
        self.result['status'] = query['status']
        try:
            aci_response_json(self.result, query['body'])
            self.module.fail_json(msg=('Query failed: %(error_code)s %(error_text)s' % self.result), **self.result)
        except KeyError:
            self.module.fail_json(msg=('Query failed for %(url)s. %(msg)s' % query))
    query = json.loads(resp.read())
    return (json.dumps(query['imdata'], sort_keys=True, indent=2) + '\n')
