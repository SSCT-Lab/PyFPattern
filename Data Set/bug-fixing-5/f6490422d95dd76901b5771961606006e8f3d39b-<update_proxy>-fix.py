def update_proxy(self, proxy_id, data):
    try:
        if self._module.check_mode:
            self._zapi.logout()
            self._module.exit_json(changed=True)
        parameters = {
            'proxyid': proxy_id,
        }
        for item in data:
            if (data[item] and (item in self.existing_data) and (self.existing_data[item] != data[item])):
                parameters[item] = data[item]
        if ('interface' in parameters):
            parameters.pop('interface')
        if (('interface' in data) and (data['status'] == '6')):
            new_interface = self.compile_interface_params(data['interface'])
            if (len(new_interface) > 0):
                parameters['interface'] = new_interface
        if (len(parameters) > 1):
            self._zapi.proxy.update(parameters)
            self._zapi.logout()
            self._module.exit_json(changed=True, result=('Successfully updated proxy %s (%s)' % (data['host'], proxy_id)))
        else:
            self._zapi.logout()
            self._module.exit_json(changed=False)
    except Exception as e:
        self._zapi.logout()
        self._module.fail_json(msg=('Failed to update proxy %s: %s' % (data['host'], e)))