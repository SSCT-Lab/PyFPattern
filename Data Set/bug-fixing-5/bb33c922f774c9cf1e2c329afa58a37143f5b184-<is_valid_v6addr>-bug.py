def is_valid_v6addr(addr):
    'check if ipv6 addr is valid'
    if (addr.find(':') != (- 1)):
        addr_list = addr.split(':')
        if (len(addr_list) > 6):
            return False
        if (addr_list[1] != ''):
            return False
        return True
    return False