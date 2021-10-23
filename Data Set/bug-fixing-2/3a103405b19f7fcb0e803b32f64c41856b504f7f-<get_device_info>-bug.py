

def get_device_info(self):
    device_info = {
        
    }
    device_info['network_os'] = 'iosxr'
    reply = self.get('show version | utility head -n 20')
    data = to_text(reply, errors='surrogate_or_strict').strip()
    match = re.search('Version (\\S+)$', data, re.M)
    if match:
        device_info['network_os_version'] = match.group(1)
    match = re.search('image file is "(.+)"', data)
    if match:
        device_info['network_os_image'] = match.group(1)
    model_search_strs = ['^Cisco (.+) \\(revision', '^[Cc]isco (\\S+ \\S+).+bytes of .*memory']
    for item in model_search_strs:
        match = re.search(item, data, re.M)
        if match:
            device_info['network_os_model'] = match.group(1)
            break
    match = re.search('^(.+) uptime', data, re.M)
    if match:
        device_info['network_os_hostname'] = match.group(1)
    return device_info
