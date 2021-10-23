def get_device_info(self):
    device_info = {
        
    }
    device_info['network_os'] = 'eos'
    reply = self.get('show version | json')
    data = json.loads(reply)
    device_info['network_os_version'] = data['version']
    device_info['network_os_model'] = data['modelName']
    reply = self.get('show hostname | json')
    data = json.loads(reply)
    device_info['network_os_hostname'] = data['hostname']
    try:
        reply = self.get('bash timeout 5 cat /mnt/flash/boot-config')
        match = re.search('SWI=(.+)$', reply, re.M)
        if match:
            device_info['network_os_image'] = match.group(1)
    except AnsibleConnectionFailure:
        self._connection.queue_message('vvv', 'Unable to gather network_os_image without enable mode')
    return device_info