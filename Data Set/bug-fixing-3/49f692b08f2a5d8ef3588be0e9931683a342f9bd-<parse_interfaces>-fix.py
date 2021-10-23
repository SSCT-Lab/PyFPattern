def parse_interfaces(configobj):
    vrf_cfg = 'vrf forwarding'
    interfaces = dict()
    for intf in set(re.findall('^interface .+', str(configobj), re.M)):
        for line in configobj[intf].children:
            if (vrf_cfg in line):
                try:
                    interfaces[line.split()[(- 1)]].append(intf.split(' ')[1])
                except KeyError:
                    interfaces[line.split()[(- 1)]] = [intf.split(' ')[1]]
    return interfaces