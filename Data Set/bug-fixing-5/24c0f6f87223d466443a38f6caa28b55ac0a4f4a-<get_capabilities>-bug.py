def get_capabilities(self):
    result = dict()
    result['rpc'] = (self.get_base_rpc() + ['edit_banner'])
    result['network_api'] = 'cliconf'
    result['device_info'] = self.get_device_info()
    result['device_operations'] = self.get_device_operations()
    result.update(self.get_options())
    return json.dumps(result)