@property
def destination_ip(self):
    if (self._values['address'] is None):
        return None
    try:
        pattern = '(?P<rd>%[0-9]+)'
        addr = re.sub(pattern, '', self._values['address'])
        ip = netaddr.IPNetwork(addr)
        return '{0}/{1}'.format(ip.ip, ip.prefixlen)
    except netaddr.AddrFormatError:
        raise F5ModuleError('The provided destination is not an IP address')