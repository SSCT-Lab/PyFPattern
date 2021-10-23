def convert_ip_prefix(self):
    'convert prefix to real value i.e. 2.2.2.2/24 to 2.2.2.0/24'
    if (self.aftype == 'v4'):
        if (self.prefix.find('.') == (- 1)):
            return False
        if (self.mask == '32'):
            return True
        if (self.mask == '0'):
            self.prefix = '0.0.0.0'
            return True
        addr_list = self.prefix.split('.')
        length = len(addr_list)
        if (length > 4):
            return False
        for each_num in addr_list:
            if (not each_num.isdigit()):
                return False
            if (int(each_num) > 255):
                return False
        byte_len = 8
        ip_len = (int(self.mask) / byte_len)
        ip_bit = (int(self.mask) % byte_len)
    else:
        if (self.prefix.find(':') == (- 1)):
            return False
        if (self.mask == '128'):
            return True
        if (self.mask == '0'):
            self.prefix = '::'
            return True
        addr_list = self.prefix.split(':')
        length = len(addr_list)
        if (length > 6):
            return False
        byte_len = 16
        ip_len = (int(self.mask) / byte_len)
        ip_bit = (int(self.mask) % byte_len)
    if (self.aftype == 'v4'):
        for i in range((ip_len + 1), length):
            addr_list[i] = 0
    else:
        for i in range((length - ip_len), length):
            addr_list[i] = 0
    for j in range(0, (byte_len - ip_bit)):
        if (self.aftype == 'v4'):
            addr_list[ip_len] = (int(addr_list[ip_len]) & (0 << j))
        else:
            if (addr_list[((length - ip_len) - 1)] == ''):
                continue
            addr_list[((length - ip_len) - 1)] = ('0x%s' % addr_list[((length - ip_len) - 1)])
            addr_list[((length - ip_len) - 1)] = (int(addr_list[((length - ip_len) - 1)], 16) & (0 << j))
    if (self.aftype == 'v4'):
        self.prefix = ('%s.%s.%s.%s' % (addr_list[0], addr_list[1], addr_list[2], addr_list[3]))
        return True
    else:
        ipv6_addr_str = ''
        for num in range(0, (length - ip_len)):
            ipv6_addr_str += ('%s:' % addr_list[num])
        self.prefix = ipv6_addr_str
        return True