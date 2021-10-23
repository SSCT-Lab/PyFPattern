def __init__(self):
    ' Main execution path '
    if (not HAS_AOS_PYEZ):
        raise Exception('aos-pyez is not installed.  Please see details here: https://github.com/Apstra/aos-pyez')
    self.inventory = dict()
    self.inventory['_meta'] = dict()
    self.inventory['_meta']['hostvars'] = dict()
    self.read_settings()
    self.parse_cli_args()
    aos = Session(server=self.aos_server, port=self.aos_server_port, user=self.aos_username, passwd=self.aos_password)
    aos.login()
    self.add_var_to_group('all', 'aos_session', aos.session)
    if self.aos_blueprint:
        bp = aos.Blueprints[self.aos_blueprint]
        if (bp.exists is False):
            fail(('Unable to find the Blueprint: %s' % self.aos_blueprint))
        for (dev_name, dev_id) in bp.params['devices'].value.items():
            self.add_host_to_group('all', dev_name)
            device = aos.Devices.find(uid=dev_id)
            if ('facts' in device.value.keys()):
                self.add_device_facts_to_var(dev_name, device)
            for node in bp.contents['system']['nodes']:
                if (node['display_name'] == dev_name):
                    self.add_host_to_group(node['role'], dev_name)
                    attributes_to_import = ['loopback_ip', 'asn', 'role', 'position']
                    for attr in attributes_to_import:
                        if (attr in node.keys()):
                            self.add_var_to_host(dev_name, attr, node[attr])
            if self.aos_blueprint_int:
                interfaces = dict()
                for link in bp.contents['system']['links']:
                    peer_id = 1
                    for side in link['endpoints']:
                        if (side['display_name'] == dev_name):
                            int_name = side['interface']
                            interfaces[int_name] = dict()
                            if ('ip' in side.keys()):
                                interfaces[int_name]['ip'] = side['ip']
                            if ('interface' in side.keys()):
                                interfaces[int_name]['name'] = side['interface']
                            if ('display_name' in link['endpoints'][peer_id].keys()):
                                interfaces[int_name]['peer'] = link['endpoints'][peer_id]['display_name']
                            if ('ip' in link['endpoints'][peer_id].keys()):
                                interfaces[int_name]['peer_ip'] = link['endpoints'][peer_id]['ip']
                            if ('type' in link['endpoints'][peer_id].keys()):
                                interfaces[int_name]['peer_type'] = link['endpoints'][peer_id]['type']
                        else:
                            peer_id = 0
                self.add_var_to_host(dev_name, 'interfaces', interfaces)
    else:
        for device in aos.Devices:
            self.add_host_to_group('all', device.name)
            if ('status' in device.value.keys()):
                for (key, value) in device.value['status'].items():
                    self.add_var_to_host(device.name, key, value)
            if ('user_config' in device.value.keys()):
                for (key, value) in device.value['user_config'].items():
                    self.add_var_to_host(device.name, key, value)
            if (device.value['status']['comm_state'] == 'on'):
                if ('facts' in device.value.keys()):
                    self.add_device_facts_to_var(device.name, device)
            if ('blueprint_active' in device.value['status'].keys()):
                if ('blueprint_id' in device.value['status'].keys()):
                    bp = aos.Blueprints.find(uid=device.value['status']['blueprint_id'])
                    if bp:
                        self.add_host_to_group(bp.name, device.name)
    data_to_print = ''
    data_to_print += self.json_format_dict(self.inventory, True)
    print(data_to_print)