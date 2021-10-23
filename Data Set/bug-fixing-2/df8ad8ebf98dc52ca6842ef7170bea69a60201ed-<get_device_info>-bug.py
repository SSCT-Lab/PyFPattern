

def get_device_info(self):
    device_info = {
        
    }
    device_info['network_os'] = 'nxos'
    reply = self.get('show version')
    platform_reply = self.get('show inventory')
    match_sys_ver = re.search('\\s+system:\\s+version (\\S+)', reply, re.M)
    if match_sys_ver:
        device_info['network_os_version'] = match_sys_ver.group(1)
    else:
        match_kick_ver = re.search('\\s+kickstart:\\s+version (\\S+)', reply, re.M)
        if match_kick_ver:
            device_info['network_os_version'] = match_kick_ver.group(1)
    if ('network_os_version' not in device_info):
        match_sys_ver = re.search('\\s+NXOS:\\s+version (\\S+)', reply, re.M)
        if match_sys_ver:
            device_info['network_os_version'] = match_sys_ver.group(1)
    match_chassis_id = re.search('Hardware\\n\\s+cisco\\s+(\\S+\\s+\\S+)', reply, re.M)
    if match_chassis_id:
        device_info['network_os_model'] = match_chassis_id.group(1)
    match_host_name = re.search('\\s+Device name:\\s+(\\S+)', reply, re.M)
    if match_host_name:
        device_info['network_os_hostname'] = match_host_name.group(1)
    match_isan_file_name = re.search('\\s+system image file is:\\s+(\\S+)', reply, re.M)
    if match_isan_file_name:
        device_info['network_os_image'] = match_isan_file_name.group(1)
    else:
        match_kick_file_name = re.search('\\s+kickstart image file is:\\s+(\\S+)', reply, re.M)
        if match_kick_file_name:
            device_info['network_os_image'] = match_kick_file_name.group(1)
    if ('network_os_image' not in device_info):
        match_isan_file_name = re.search('\\s+NXOS image file is:\\s+(\\S+)', reply, re.M)
        if match_isan_file_name:
            device_info['network_os_image'] = match_isan_file_name.group(1)
    match_os_platform = re.search('NAME: "Chassis",\\s+DESCR: "NX-OSv Chassis\\s?"\\s+\\nPID:\\s+(\\S+)', platform_reply, re.M)
    if match_os_platform:
        device_info['network_os_platform'] = match_os_platform.group(1)
    return device_info
