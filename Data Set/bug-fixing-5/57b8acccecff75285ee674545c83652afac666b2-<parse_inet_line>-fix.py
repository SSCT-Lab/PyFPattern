def parse_inet_line(self, words, current_if, ips):
    if (words[1] == 'alias'):
        del words[1]
    address = {
        'address': words[1],
    }
    if (re.match('([0-9a-f]){8}', words[3]) and (len(words[3]) == 8)):
        words[3] = ('0x' + words[3])
    if words[3].startswith('0x'):
        address['netmask'] = socket.inet_ntoa(struct.pack('!L', int(words[3], base=16)))
    else:
        address['netmask'] = words[3]
    address_bin = struct.unpack('!L', socket.inet_aton(address['address']))[0]
    netmask_bin = struct.unpack('!L', socket.inet_aton(address['netmask']))[0]
    address['network'] = socket.inet_ntoa(struct.pack('!L', (address_bin & netmask_bin)))
    if (len(words) > 5):
        address['broadcast'] = words[5]
    else:
        address['broadcast'] = socket.inet_ntoa(struct.pack('!L', (address_bin | ((~ netmask_bin) & 4294967295))))
    if (not words[1].startswith('127.')):
        ips['all_ipv4_addresses'].append(address['address'])
    current_if['ipv4'].append(address)