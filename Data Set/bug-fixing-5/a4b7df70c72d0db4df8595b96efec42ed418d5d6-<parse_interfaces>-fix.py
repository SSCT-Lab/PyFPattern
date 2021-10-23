def parse_interfaces(module, vlan):
    vlan_int = []
    interfaces = vlan.get('vlanshowplist-ifidx')
    if interfaces:
        for i in interfaces.split(','):
            if (('eth' in i.lower()) and ('-' in i)):
                int_range = i.split('-')
                stop = int(int_range[1])
                start = int(int_range[0].split('/')[1])
                eth = int_range[0].split('/')[0]
                for r in range(start, (stop + 1)):
                    vlan_int.append(((eth + '/') + str(r)))
            else:
                vlan_int.append(i)
    return vlan_int