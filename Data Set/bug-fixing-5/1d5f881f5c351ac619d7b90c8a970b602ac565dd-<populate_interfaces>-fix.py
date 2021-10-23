def populate_interfaces(self, interfaces):
    facts = dict()
    for (key, value) in iteritems(interfaces):
        intf = dict()
        if (get_interface_type(key) == 'svi'):
            intf['state'] = self.parse_state(key, value, intf_type='svi')
            intf['macaddress'] = self.parse_macaddress(value, intf_type='svi')
            intf['mtu'] = self.parse_mtu(value, intf_type='svi')
            intf['bandwidth'] = self.parse_bandwidth(value, intf_type='svi')
            intf['type'] = self.parse_type(value, intf_type='svi')
            if ('Internet Address' in value):
                intf['ipv4'] = self.parse_ipv4_address(value, intf_type='svi')
            facts[key] = intf
        else:
            intf['state'] = self.parse_state(key, value)
            intf['description'] = self.parse_description(value)
            intf['macaddress'] = self.parse_macaddress(value)
            intf['mode'] = self.parse_mode(value)
            intf['mtu'] = self.parse_mtu(value)
            intf['bandwidth'] = self.parse_bandwidth(value)
            intf['duplex'] = self.parse_duplex(value)
            intf['speed'] = self.parse_speed(value)
            intf['type'] = self.parse_type(value)
            if ('Internet Address' in value):
                intf['ipv4'] = self.parse_ipv4_address(value)
            facts[key] = intf
    return facts