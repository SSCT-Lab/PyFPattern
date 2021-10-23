

def get_interfaces_dict(self):
    ' get interfaces attributes dict.'
    intfs_info = dict()
    conf_str = CE_NC_GET_INTFS
    recv_xml = get_nc_config(self.module, conf_str)
    if ('<data/>' in recv_xml):
        return intfs_info
    xml_str = recv_xml.replace('\r', '').replace('\n', '').replace('xmlns="urn:ietf:params:xml:ns:netconf:base:1.0"', '').replace('xmlns="http://www.huawei.com/netconf/vrp"', '')
    root = ElementTree.fromstring(xml_str)
    intfs = root.findall('ifm/interfaces/')
    if intfs:
        for intf in intfs:
            intf_type = intf.find('ifPhyType').text.lower()
            if intf_type:
                if (not intfs_info.get(intf_type)):
                    intfs_info[intf_type] = list()
                intf_info = dict()
                for tmp in intf:
                    intf_info[tmp.tag] = tmp.text
                intfs_info[intf_type].append(intf_info)
    return intfs_info
