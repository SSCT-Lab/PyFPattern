def add_proxy(self, data):
    try:
        if self._module.check_mode:
            self._zapi.logout()
            self._module.exit_json(changed=True)
        parameters = {
            
        }
        for item in data:
            if data[item]:
                parameters[item] = data[item]
        proxy_ids_list = self._zapi.proxy.create(parameters)
        self._zapi.logout()
        self._module.exit_json(changed=True, result=('Successfully added proxy %s (%s)' % (data['host'], data['status'])))
        if (len(proxy_ids_list) >= 1):
            return proxy_ids_list['proxyids'][0]
    except Exception as e:
        self._zapi.logout()
        self._module.fail_json(msg=('Failed to create proxy %s: %s' % (data['host'], e)))