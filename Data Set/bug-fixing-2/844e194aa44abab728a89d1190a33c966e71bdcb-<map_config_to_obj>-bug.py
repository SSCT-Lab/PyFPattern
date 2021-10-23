

def map_config_to_obj(self):
    data = get_config(self._module, config_filter='interface')
    interfaces = data.strip().rstrip('!').split('!')
    if (not interfaces):
        return list()
    for interface in interfaces:
        intf_config = interface.strip().splitlines()
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
