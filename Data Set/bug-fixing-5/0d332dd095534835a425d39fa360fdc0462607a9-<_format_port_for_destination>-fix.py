def _format_port_for_destination(self, ip, port):
    if validate_ip_v6_address(ip):
        if (port == 0):
            result = '.any'
        else:
            result = '.{0}'.format(port)
    else:
        result = ':{0}'.format(port)
    return result