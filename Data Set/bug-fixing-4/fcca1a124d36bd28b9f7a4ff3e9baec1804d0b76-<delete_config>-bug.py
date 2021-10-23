def delete_config(self):
    '\n        This method is used to handle the logic when the modules state is equal to absent. The method only pushes a change if\n        the object exists, and if check_mode is False. A successful change will mark the module as changed.\n        '
    self.proposed = dict()
    if (not self.existing):
        return
    elif (not self.module.check_mode):
        if (not self.params['private_key']):
            self.cert_auth(method='DELETE')
        (resp, info) = fetch_url(self.module, self.url, headers=self.headers, method='DELETE', timeout=self.params['timeout'], use_proxy=self.params['use_proxy'])
        self.response = info['msg']
        self.status = info['status']
        self.method = 'DELETE'
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
        self.method = 'DELETE'