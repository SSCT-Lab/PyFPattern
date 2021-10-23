def populate_interfaces(self, data):
    interfaces = dict()
    for item in data['TABLE_interface']['ROW_interface']:
        name = item['interface']
        intf = dict()
        if ('type' in item):
            intf.update(self.transform_dict(item, self.INTERFACE_SVI_MAP))
        else:
            intf.update(self.transform_dict(item, self.INTERFACE_MAP))
        if ('eth_ip_addr' in item):
            intf['ipv4'] = self.transform_dict(item, self.INTERFACE_IPV4_MAP)
            self.facts['all_ipv4_addresses'].append(item['eth_ip_addr'])
        if ('svi_ip_addr' in item):
            intf['ipv4'] = self.transform_dict(item, self.INTERFACE_SVI_IPV4_MAP)
            self.facts['all_ipv4_addresses'].append(item['svi_ip_addr'])
        interfaces[name] = intf
    return interfaces