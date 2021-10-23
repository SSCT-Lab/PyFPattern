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
    return True