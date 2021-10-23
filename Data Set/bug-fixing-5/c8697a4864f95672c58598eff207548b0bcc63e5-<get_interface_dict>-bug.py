def get_interface_dict(self, ifname):
    ' get one interface attributes dict.'
    intf_info = dict()
    conf_str = (CE_NC_GET_PORT_ATTR % ifname)
    rcv_xml = get_nc_config(self.module, conf_str)
    if ('<data/>' in rcv_xml):
        return intf_info
    intf = re.findall('.*<ifName>(.*)</ifName>.*\\s*<l2Enable>(.*)</l2Enable>.*', rcv_xml)
    if intf:
        intf_info = dict(ifName=intf[0][0], l2Enable=intf[0][1], linkType='', pvid='', trunkVlans='')
        if (intf_info['l2Enable'] == 'enable'):
            attr = re.findall('.*<linkType>(.*)</linkType>.*.*\\s*<pvid>(.*)</pvid>.*\\s*<trunkVlans>(.*)</trunkVlans>.*', rcv_xml)
            if attr:
                intf_info['linkType'] = attr[0][0]
                intf_info['pvid'] = attr[0][1]
                intf_info['trunkVlans'] = attr[0][2]
    return intf_info