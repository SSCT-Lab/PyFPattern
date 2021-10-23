def get_device_info(self):
    if self._device_info:
        return self._device_info
    device_info = {
        
    }
    device_info['network_os'] = 'eos'
    reply = self.send_request('show version', output='json')
    data = json.loads(reply)
    device_info['network_os_version'] = data['version']
    device_info['network_os_model'] = data['modelName']
    reply = self.send_request('show hostname | json')
    data = json.loads(reply)
    device_info['network_os_hostname'] = data['hostname']
    self._device_info = device_info
    return self._device_info