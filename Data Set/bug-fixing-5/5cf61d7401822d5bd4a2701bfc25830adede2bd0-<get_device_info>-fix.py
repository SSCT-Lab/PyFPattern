def get_device_info(self):
    device_info = {
        
    }
    device_info['network_os'] = 'ios'
    reply = self.get('show version')
    data = to_text(reply, errors='surrogate_or_strict').strip()
    match = re.search('Version (\\S+)', data)
    if match:
        device_info['network_os_version'] = match.group(1).strip(',')
    match = re.search('^Cisco (.+) \\(revision', data, re.M)
    if match:
        device_info['network_os_model'] = match.group(1)
    match = re.search('^(.+) uptime', data, re.M)
    if match:
        device_info['network_os_hostname'] = match.group(1)
    return device_info