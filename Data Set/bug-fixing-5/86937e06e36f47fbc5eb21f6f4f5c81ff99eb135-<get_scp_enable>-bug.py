def get_scp_enable(self):
    'Get scp enable state'
    xml_str = CE_NC_GET_SCP_ENABLE
    scp_enable = dict()
    ret_xml = get_nc_config(self.module, xml_str)
    if ('<data/>' in ret_xml):
        return scp_enable
    xml_str = ret_xml.replace('\r', '').replace('\n', '').replace('xmlns="urn:ietf:params:xml:ns:netconf:base:1.0"', '').replace('xmlns="http://www.huawei.com/netconf/vrp"', '')
    root = ElementTree.fromstring(xml_str)
    topo = root.find('sshs/sshServerEnable')
    if (topo is None):
        return scp_enable
    for eles in topo:
        scp_enable[eles.tag] = eles.text
    return scp_enable