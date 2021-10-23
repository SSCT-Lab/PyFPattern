def get_peer_link_info(self):
    ' get peer link info.'
    peer_link_info = dict()
    conf_str = CE_NC_GET_PEER_LINK_INFO
    xml_str = get_nc_config(self.module, conf_str)
    if ('<data/>' in xml_str):
        return peer_link_info
    else:
        xml_str = xml_str.replace('\r', '').replace('\n', '').replace('xmlns="urn:ietf:params:xml:ns:netconf:base:1.0"', '').replace('xmlns="http://www.huawei.com/netconf/vrp"', '')
        root = ElementTree.fromstring(xml_str)
        link_info = root.findall('data/mlag/peerlinks/peerlink')
        if link_info:
            for tmp in link_info:
                for site in tmp:
                    if (site.tag in ['linkId', 'portName']):
                        peer_link_info[site.tag] = site.text
        return peer_link_info