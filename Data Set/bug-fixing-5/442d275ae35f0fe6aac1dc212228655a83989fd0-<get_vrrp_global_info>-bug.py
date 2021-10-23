def get_vrrp_global_info(self):
    ' get vrrp global info.'
    vrrp_global_info = dict()
    conf_str = CE_NC_GET_VRRP_GLOBAL_INFO
    xml_str = get_nc_config(self.module, conf_str)
    if ('<data/>' in xml_str):
        return vrrp_global_info
    else:
        xml_str = xml_str.replace('\r', '').replace('\n', '').replace('xmlns="urn:ietf:params:xml:ns:netconf:base:1.0"', '').replace('xmlns="http://www.huawei.com/netconf/vrp"', '')
        root = ElementTree.fromstring(xml_str)
        global_info = root.findall('data/vrrp/vrrpGlobalCfg')
        if global_info:
            for tmp in global_info:
                for site in tmp:
                    if (site.tag in ['gratuitousArpTimeOut', 'gratuitousArpFlag', 'recoverDelay', 'version']):
                        vrrp_global_info[site.tag] = site.text
        return vrrp_global_info