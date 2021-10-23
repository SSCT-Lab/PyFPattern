def parse_interfaces(configobj, name):
    vrf_cfg = ('vrf forwarding %s' % name)
    interfaces = list()
    for intf in re.findall('^interface .+', str(configobj), re.M):
        if (vrf_cfg in '\n'.join(configobj[intf].children)):
            interfaces.append(intf.split(' ')[1])
    return interfaces