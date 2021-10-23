def _format_port_for_destination(self, ip, port):
    addr = netaddr.IPAddress(ip)
    if (addr.version == 6):
        if (port == 0):
            result = '.any'
        else:
            result = '.{0}'.format(port)
    else:
        result = ':{0}'.format(port)
    return result