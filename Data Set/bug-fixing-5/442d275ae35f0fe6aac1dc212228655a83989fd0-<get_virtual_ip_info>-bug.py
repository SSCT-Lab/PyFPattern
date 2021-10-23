def get_virtual_ip_info(self):
    ' get vrrp virtual ip info.'
    virtual_ip_info = dict()
    conf_str = (CE_NC_GET_VRRP_VIRTUAL_IP_INFO % (self.vrid, self.interface))
    xml_str = get_nc_config(self.module, conf_str)
    if ('<data/>' in xml_str):
        return virtual_ip_info
    else:
        xml_str = xml_str.replace('\r', '').replace('\n', '').replace('xmlns="urn:ietf:params:xml:ns:netconf:base:1.0"', '').replace('xmlns="http://www.huawei.com/netconf/vrp"', '')
        virtual_ip_info['vrrpVirtualIpInfos'] = list()
        root = ElementTree.fromstring(xml_str)
        vrrp_virtual_ip_infos = root.findall('data/vrrp/vrrpGroups/vrrpGroup/virtualIps/virtualIp')
        if vrrp_virtual_ip_infos:
            for vrrp_virtual_ip_info in vrrp_virtual_ip_infos:
                virtual_ip_dict = dict()
                for ele in vrrp_virtual_ip_info:
                    if (ele.tag in ['virtualIpAddress']):
                        virtual_ip_dict[ele.tag] = ele.text
                virtual_ip_info['vrrpVirtualIpInfos'].append(virtual_ip_dict)
        return virtual_ip_info