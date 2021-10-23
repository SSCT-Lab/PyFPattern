def get_interface_dict(self, ifname):
    ' get one interface attributes dict.'
    intf_info = dict()
    conf_str = (CE_NC_GET_INTF % ifname)
    ret_xml = get_nc_config(self.module, conf_str)
    if ('<data/>' in ret_xml):
        return intf_info
    intf = re.findall('.*<ifName>(.*)</ifName>.*\\s*<isL2SwitchPort>(.*)</isL2SwitchPort>.*\\s*<ifMtu>(.*)</ifMtu>.*', ret_xml)
    if intf:
        intf_info = dict(ifName=intf[0][0], isL2SwitchPort=intf[0][1], ifMtu=intf[0][2])
    return intf_info