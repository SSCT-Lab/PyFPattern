def check_macaddr(self):
    'check mac-address whether valid'
    valid_char = '0123456789abcdef-'
    mac = self.mlag_system_id
    if (len(mac) > 16):
        return False
    mac_list = re.findall('([0-9a-fA-F]+)', mac)
    if (len(mac_list) != 3):
        return False
    if (mac.count('-') != 2):
        return False
    for (_, value) in enumerate(mac, start=0):
        if (value.lower() not in valid_char):
            return False
    if all(((int(mac_list[0], base=16) == 0), (int(mac_list[1], base=16) == 0), (int(mac_list[2], base=16) == 0))):
        return False
    a = ('000' + mac_list[0])
    b = ('000' + mac_list[1])
    c = ('000' + mac_list[2])
    self.mlag_system_id = '-'.join([a[(- 4):], b[(- 4):], c[(- 4):]])
    return True