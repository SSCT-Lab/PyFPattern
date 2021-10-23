def get_bfd_dict(self):
    'bfd config dict'
    bfd_dict = dict()
    bfd_dict['global'] = dict()
    bfd_dict['session'] = dict()
    conf_str = (CE_NC_GET_BFD % (CE_NC_GET_BFD_GLB + (CE_NC_GET_BFD_SESSION % self.session_name)))
    xml_str = get_nc_config(self.module, conf_str)
    if ('<data/>' in xml_str):
        return bfd_dict
    xml_str = xml_str.replace('\r', '').replace('\n', '').replace('xmlns="urn:ietf:params:xml:ns:netconf:base:1.0"', '').replace('xmlns="http://www.huawei.com/netconf/vrp"', '')
    root = ElementTree.fromstring(xml_str)
    glb = root.find('data/bfd/bfdSchGlobal')
    if glb:
        for attr in glb:
            bfd_dict['global'][attr.tag] = attr.text
    sess = root.find('data/bfd/bfdCfgSessions/bfdCfgSession')
    if sess:
        for attr in sess:
            bfd_dict['session'][attr.tag] = attr.text
    return bfd_dict