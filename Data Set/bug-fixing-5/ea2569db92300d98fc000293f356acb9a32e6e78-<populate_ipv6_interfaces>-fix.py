def populate_ipv6_interfaces(self, data):
    for (key, value) in iteritems(data):
        if ((key in ['No', 'RPF']) or key.startswith('IP')):
            continue
        self.facts['interfaces'][key]['ipv6'] = list()
        addresses = re.findall('\\s+(.+), subnet', value, re.M)
        subnets = re.findall(', subnet is (.+)$', value, re.M)
        for (addr, subnet) in zip(addresses, subnets):
            ipv6 = dict(address=addr.strip(), subnet=subnet.strip())
            self.add_ip_address(addr.strip(), 'ipv6')
            self.facts['interfaces'][key]['ipv6'].append(ipv6)