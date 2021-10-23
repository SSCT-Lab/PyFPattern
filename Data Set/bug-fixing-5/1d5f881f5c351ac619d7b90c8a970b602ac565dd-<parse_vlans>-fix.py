def parse_vlans(self, data):
    objects = list()
    for line in data.splitlines():
        if (line == ''):
            continue
        if line[0].isdigit():
            vlan = line.split()[0]
            objects.append(vlan)
    return objects