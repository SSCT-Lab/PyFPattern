def get_device_info(self):
    device_info = {
        
    }
    device_info['network_os'] = 'iosxr'
    install_meta = collections.OrderedDict()
    install_meta.update([('boot-variables', {
        'xpath': 'install/boot-variables',
        'tag': True,
    }), ('boot-variable', {
        'xpath': 'install/boot-variables/boot-variable',
        'tag': True,
        'lead': True,
    }), ('software', {
        'xpath': 'install/software',
        'tag': True,
    }), ('alias-devices', {
        'xpath': 'install/software/alias-devices',
        'tag': True,
    }), ('alias-device', {
        'xpath': 'install/software/alias-devices/alias-device',
        'tag': True,
    }), ('m:device-name', {
        'xpath': 'install/software/alias-devices/alias-device/device-name',
        'value': 'disk0:',
    })])
    install_filter = build_xml('install', install_meta, opcode='filter')
    try:
        reply = self.get(install_filter)
        resp = remove_namespaces(re.sub('<\\?xml version="1.0" encoding="UTF-8"\\?>', '', reply))
        ele_boot_variable = etree_find(resp, 'boot-variable/boot-variable')
        if (ele_boot_variable is not None):
            device_info['network_os_image'] = re.split('[:|,]', ele_boot_variable.text)[1]
        ele_package_name = etree_find(reply, 'package-name')
        if (ele_package_name is not None):
            device_info['network_os_package'] = ele_package_name.text
            device_info['network_os_version'] = re.split('-', ele_package_name.text)[(- 1)]
        hostname_filter = build_xml('host-names', opcode='filter')
        reply = self.get(hostname_filter)
        resp = remove_namespaces(re.sub('<\\?xml version="1.0" encoding="UTF-8"\\?>', '', reply))
        hostname_ele = etree_find(resp.strip(), 'host-name')
        device_info['network_os_hostname'] = (hostname_ele.text if (hostname_ele is not None) else None)
    except Exception as exc:
        self._connection.queue_message('vvvv', ('Fail to retrieve device info %s' % exc))
    return device_info