

def delete_config(self):
    '\n        This method is used to handle the logic when the modules state is equal to absent. The method only pushes a change if\n        the object exists, and if check_mode is Fasle. A successful change will mark the module as changed.\n        '
    self.result['proposed'] = {
        
    }
    if (not self.result['existing']):
        return
    elif (not self.module.check_mode):
        (resp, info) = fetch_url(self.module, self.result['url'], headers=self.headers, method='DELETE', timeout=self.params['timeout'], use_proxy=self.params['use_proxy'])
        self.result['response'] = info['msg']
        self.result['status'] = info['status']
        self.result['method'] = 'DELETE'
        if (info['status'] == 200):
            self.result['changed'] = True
            aci_response_json(self.result, resp.read())
        else:
            try:
                aci_response_json(self.result, info['body'])
                self.module.fail_json(msg=('Request failed: %(error_code)s %(error_text)s' % self.result), **self.result)
            except KeyError:
                self.module.fail_json(msg=('Request failed for %(url)s. %(msg)s' % info))
    else:
        self.result['changed'] = True
        self.result['method'] = 'DELETE'
