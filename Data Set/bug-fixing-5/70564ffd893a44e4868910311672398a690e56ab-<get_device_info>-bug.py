def get_device_info(self):
    device_info = {
        
    }
    device_info['network_os'] = 'slxos'
    reply = self.get(b'show version')
    data = to_text(reply, errors='surrogate_or_strict').strip()
    match = re.search('SLX\\-OS Operating System Version: (\\S+)', data)
    if match:
        device_info['network_os_version'] = match.group(1)
    reply = self.get(b'show chassis')
    data = to_text(reply, errors='surrogate_or_strict').strip()
    match = re.search('^Chassis Name:(\\s+)(\\S+)', data, re.M)
    if match:
        device_info['network_os_model'] = match.group(2)
    reply = self.get(b'show running-config | inc "switch-attributes host-name')
    data = to_text(reply, errors='surrogate_or_strict').strip()
    match = re.search('switch-attributes host-name (\\S+)', data, re.M)
    if match:
        device_info['network_os_hostname'] = match.group(1)
    return device_info