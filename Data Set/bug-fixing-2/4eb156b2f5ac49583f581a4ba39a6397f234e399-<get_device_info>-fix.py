

def get_device_info(self):
    device_info = {
        
    }
    device_info['network_os'] = 'ios'
    reply = self.get(command='show version')
    data = to_text(reply, errors='surrogate_or_strict').strip()
    match = re.search('Version (\\S+)', data)
    if match:
        device_info['network_os_version'] = match.group(1).strip(',')
    model_search_strs = ['^[Cc]isco (.+) \\(revision', '^[Cc]isco (\\S+).+bytes of .*memory']
    for item in model_search_strs:
        match = re.search(item, data, re.M)
        if match:
            version = match.group(1).split(' ')
            device_info['network_os_model'] = version[0]
            break
    match = re.search('^(.+) uptime', data, re.M)
    if match:
        device_info['network_os_hostname'] = match.group(1)
    match = re.search('image file is "(.+)"', data)
    if match:
        device_info['network_os_image'] = match.group(1)
    return device_info
