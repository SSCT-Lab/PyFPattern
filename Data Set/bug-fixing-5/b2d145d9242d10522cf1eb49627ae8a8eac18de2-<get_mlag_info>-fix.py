def get_mlag_info(self):
    ' get mlag info.'
    mlag_info = dict()
    conf_str = (CE_NC_GET_MLAG_INFO % ('<localMlagPort>Eth-Trunk%s</localMlagPort>' % self.eth_trunk_id))
    xml_str = get_nc_config(self.module, conf_str)
    if ('<data/>' in xml_str):
        return mlag_info
    else:
        xml_str = xml_str.replace('\r', '').replace('\n', '').replace('xmlns="urn:ietf:params:xml:ns:netconf:base:1.0"', '').replace('xmlns="http://www.huawei.com/netconf/vrp"', '')
        mlag_info['mlagInfos'] = list()
        root = ElementTree.fromstring(xml_str)
        dfs_mlag_infos = root.findall('./mlag/mlagInstances/mlagInstance')
        if dfs_mlag_infos:
            for dfs_mlag_info in dfs_mlag_infos:
                mlag_dict = dict()
                for ele in dfs_mlag_info:
                    if (ele.tag in ['dfsgroupId', 'mlagId', 'localMlagPort']):
                        mlag_dict[ele.tag] = ele.text
                mlag_info['mlagInfos'].append(mlag_dict)
        return mlag_info