def parse_ipv6_address(self, interface):
    ip_address = list()
    for addr in interface.findall('./ipv6/ipv6-addresses/address'):
        ipv6_addr = addr.find('./ipv6-address')
        if (ipv6_addr is not None):
            ip_address.append(ipv6_addr.text)
            self.add_ip_address(ipv6_addr.text, 'ipv6')
    return ip_address