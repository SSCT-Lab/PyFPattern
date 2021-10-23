def get_interface_dict(self, ifname):
    ' get one interface attributes dict.'
    intf_info = dict()
    conf_str = (CE_NC_GET_PORT_ATTR % ifname)
    xml_str = get_nc_config(self.module, conf_str)
    if ('<data/>' in xml_str):
        return intf_info
    xml_str = xml_str.replace('\r', '').replace('\n', '').replace('xmlns="urn:ietf:params:xml:ns:netconf:base:1.0"', '').replace('xmlns="http://www.huawei.com/netconf/vrp"', '')
    tree = ET.fromstring(xml_str)
    l2Enable = tree.find('ethernet/ethernetIfs/ethernetIf/l2Enable')
    intf_info['l2Enable'] = l2Enable.text
    port_type = tree.find('ethernet/ethernetIfs/ethernetIf/l2Attribute')
    for pre in port_type:
        intf_info[pre.tag] = pre.text
    intf_info['ifName'] = ifname
    if (intf_info['trunkVlans'] is None):
        intf_info['trunkVlans'] = ''
    if (intf_info['untagVlans'] is None):
        intf_info['untagVlans'] = ''
    return intf_info