def get_scp_enable(self):
    'Get scp enable state'
    ret_xml = ''
    try:
        ret_xml = get_nc_config(self.module, CE_NC_GET_SCP_ENABLE)
    except ConnectionError:
        self.module.fail_json(msg='Error: The NETCONF API of scp_enable is not supported.')
    if ('<data/>' in ret_xml):
        return False
    xml_str = ret_xml.replace('\r', '').replace('\n', '').replace('xmlns="urn:ietf:params:xml:ns:netconf:base:1.0"', '').replace('xmlns="http://www.huawei.com/netconf/vrp"', '')
    root = ElementTree.fromstring(xml_str)
    topo1 = root.find('sshs/sshServer/scpEnable')
    topo2 = root.find('sshs/sshServerEnable/scpIpv4Enable')
    topo3 = root.find('sshs/sshServerEnable/scpIpv6Enable')
    if (topo1 is not None):
        return (str(topo1.text).strip().lower() == 'enable')
    elif (self.host_is_ipv6 and (topo3 is not None)):
        return (str(topo3.text).strip().lower() == 'enable')
    elif (topo2 is not None):
        return (str(topo2.text).strip().lower() == 'enable')
    return False