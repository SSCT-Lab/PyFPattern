@property
def destination_ip(self):
    if (self._values['address'] is None):
        return None
    try:
        pattern = '(?P<rd>%[0-9]+)'
        addr = re.sub(pattern, '', self._values['address'])
        ip = ip_interface('{0}'.format(addr))
        return ip.with_prefixlen
    except ValueError:
        raise F5ModuleError('The provided destination is not an IP address')