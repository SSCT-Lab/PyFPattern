

def validate_n_expand_ipv4(module, want):
    ip_addr_want = want.get('address')
    validate_ipv4(ip_addr_want, module)
    ip = ip_addr_want.split('/')
    if (len(ip) == 2):
        ip_addr_want = '{0} {1}'.format(ip[0], to_netmask(ip[1]))
    return ip_addr_want
