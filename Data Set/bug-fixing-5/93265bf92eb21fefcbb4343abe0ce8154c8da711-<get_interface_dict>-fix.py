def get_interface_dict(self, ifname):
    ' get one interface attributes dict.'
    intf_info = dict()
    flags = list()
    exp = ('| ignore-case section include ^#\\s+interface %s\\s+' % ifname.replace(' ', ''))
    flags.append(exp)
    output = self.get_config(flags)
    output_list = output.split('\n')
    if (output_list is None):
        return intf_info
    mtu = None
    for config in output_list:
        config = config.strip()
        if config.startswith('mtu'):
            mtu = re.findall('.*mtu\\s*([0-9]*)', output)[0]
    intf_info = dict(ifName=ifname, ifMtu=mtu)
    return intf_info