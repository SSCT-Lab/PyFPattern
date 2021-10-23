def get_existing(self):
    "\n        This method is used to get the existing object(s) based on the path specified in the module. Each module should\n        build the URL so that if the object's name is supplied, then it will retrieve the configuration for that particular\n        object, but if no name is supplied, then it will retrieve all MOs for the class. Following this method will ensure\n        that this method can be used to supply the existing configuration when using the get_diff method. The response, status,\n        and existing configuration will be added to the self.result dictionary.\n        "
    uri = (self.url + self.filter_string)
    if (not self.params['private_key']):
        self.cert_auth(path=(self.path + self.filter_string), method='GET')
    (resp, info) = fetch_url(self.module, uri, headers=self.headers, method='GET', timeout=self.params['timeout'], use_proxy=self.params['use_proxy'])
    self.response = info['msg']
    self.status = info['status']
    self.method = 'GET'
    if (info['status'] == 200):
        self.existing = json.loads(resp.read())['imdata']
    else:
        try:
            self.response_json(info['body'])
            self.fail_json(msg=('APIC Error %(code)s: %(text)s' % self.error))
        except KeyError:
            self.fail_json(msg=('Connection failed for %(url)s. %(msg)s' % info))