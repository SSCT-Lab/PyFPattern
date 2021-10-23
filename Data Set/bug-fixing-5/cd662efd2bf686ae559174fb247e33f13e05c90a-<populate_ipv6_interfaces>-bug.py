def populate_ipv6_interfaces(self, data):
    for (key, value) in data.items():
        self.facts['interfaces'][key]['ipv6'] = list()
        addresses = re.findall('\\s+(.+), subnet', value, re.M)
        subnets = re.findall(', subnet is (\\S+)', value, re.M)
        for (addr, subnet) in itertools.izip(addresses, subnets):
            ipv6 = dict(address=addr.strip(), subnet=subnet.strip())
            self.add_ip_address(addr.strip(), 'ipv6')
            self.facts['interfaces'][key]['ipv6'].append(ipv6)