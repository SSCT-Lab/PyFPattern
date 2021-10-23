def parse_ipv6_interfaces(self, data):
    try:
        data = data['TABLE_intf']
        if data:
            if isinstance(data, dict):
                data = [data]
            for item in data:
                name = item['ROW_intf']['intf-name']
                intf = self.facts['interfaces'][name]
                intf['ipv6'] = self.transform_dict(item, self.INTERFACE_IPV6_MAP)
                self.facts['all_ipv6_addresses'].append(item['ROW_intf']['addr'])
        else:
            return ''
    except TypeError:
        return ''