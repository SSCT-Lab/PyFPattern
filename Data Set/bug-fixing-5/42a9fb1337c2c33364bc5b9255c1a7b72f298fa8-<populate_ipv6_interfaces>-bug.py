def populate_ipv6_interfaces(self, data):
    interfaces = re.split('=+', data)[1].strip()
    matches = re.findall('(\\S+ \\S+) +[\\w-]+.+\\s+([\\d:/]+)', interfaces, re.M)
    for match in matches:
        interface = match[0]
        self.facts['interfaces'][interface]['ipv6'] = list()
        (address, masklen) = match[1].split('/')
        ipv6 = dict(address=address, masklen=int(masklen))
        self.add_ip_address(ipv6['address'], 'ipv6')
        self.facts['interfaces'][interface]['ipv6'].append(ipv6)