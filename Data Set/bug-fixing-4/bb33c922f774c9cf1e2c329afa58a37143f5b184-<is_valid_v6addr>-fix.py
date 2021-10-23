def is_valid_v6addr(addr):
    'check if ipv6 addr is valid'
    if (addr.find(':') != (- 1)):
        addr_list = addr.split(':')
        if (len(addr_list) > 8):
            return False
        if (addr.count('::') > 1):
            return False
        if ((addr.count('::') == 0) and (len(addr_list) < 8)):
            return False
        for group in addr_list:
            if (group.strip() == ''):
                continue
            try:
                int(group, base=16)
            except ValueError:
                return False
        return True
    return False