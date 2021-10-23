def post_config(self):
    '\n        This method is used to handle the logic when the modules state is equal to present. The method only pushes a change if\n        the object has differences than what exists on the APIC, and if check_mode is False. A successful change will mark the\n        module as changed.\n        '
    if (not self.config):
        return
    elif (not self.module.check_mode):
        if self.params['private_key']:
            self.cert_auth(method='POST', payload=json.dumps(self.config))
        (resp, info) = fetch_url(self.module, self.url, data=json.dumps(self.config), headers=self.headers, method='POST', timeout=self.params['timeout'], use_proxy=self.params['use_proxy'])
        self.response = info['msg']
        self.status = info['status']
        self.method = 'POST'
        if (info['status'] == 200):
            self.result['changed'] = True
            self.response_json(resp.read())
        else:
            try:
                self.response_json(info['body'])
                self.fail_json(msg=('APIC Error %(code)s: %(text)s' % self.error))
            except KeyError:
                self.fail_json(msg=('Connection failed for %(url)s. %(msg)s' % info))
    else:
        self.result['changed'] = True
        self.method = 'POST'