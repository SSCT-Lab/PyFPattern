def parse_ipv6_address(self, interface):
    ipv6 = interface.find('ipv6')
    ip_address = ''
    if (ipv6 is not None):
        ipv6_addr = ipv6.find('./address/ipv6-address')
        if (ipv6_addr is not None):
            ip_address = ipv6_addr.text
            self.add_ip_address(ip_address, 'ipv6')
    return ip_address