def map_config_to_obj(self):
    data = get_config(self._module, config_filter='interface')
    data_lines = data.splitlines()
    start_indexes = [i for (i, e) in enumerate(data_lines) if e.startswith('interface')]
    end_indexes = [i for (i, e) in enumerate(data_lines) if (e == '!')]
    intf_configs = list()
    for (start_index, end_index) in zip(start_indexes, end_indexes):
        intf_configs.append([i.strip() for i in data_lines[start_index:end_index]])
    if (not intf_configs):
        return list()
    for intf_config in intf_configs:
        name = intf_config[0].strip().split()[1]
        active = 'act'
        if (name == 'preconfigure'):
            active = 'pre'
            name = intf_config[0].strip().split()[2]
        obj = {
            'name': name,
            'description': self.parse_config_argument(intf_config, 'description'),
            'speed': self.parse_config_argument(intf_config, 'speed'),
            'duplex': self.parse_config_argument(intf_config, 'duplex'),
            'mtu': self.parse_config_argument(intf_config, 'mtu'),
            'enabled': (True if (not self.parse_shutdown(intf_config)) else False),
            'active': active,
            'state': 'present',
        }
        self._have.append(obj)