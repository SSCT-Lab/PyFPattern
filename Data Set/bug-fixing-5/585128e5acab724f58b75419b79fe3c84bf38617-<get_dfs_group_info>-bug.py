def get_dfs_group_info(self):
    ' get dfs group attributes info.'
    dfs_group_info = dict()
    conf_str = CE_NC_GET_DFS_GROUP_INFO
    xml_str = get_nc_config(self.module, conf_str)
    if ('<data/>' in xml_str):
        return dfs_group_info
    else:
        xml_str = xml_str.replace('\r', '').replace('\n', '').replace('xmlns="urn:ietf:params:xml:ns:netconf:base:1.0"', '').replace('xmlns="http://www.huawei.com/netconf/vrp"', '')
        root = ElementTree.fromstring(xml_str)
        dfs_info = root.findall('data/dfs/groupInstances/groupInstance')
        if dfs_info:
            for tmp in dfs_info:
                for site in tmp:
                    if (site.tag in ['groupId', 'priority', 'ipAddress', 'srcVpnName']):
                        dfs_group_info[site.tag] = site.text
        dfs_nick_info = root.findall('data/dfs/groupInstances/groupInstance/trillType')
        if dfs_nick_info:
            for tmp in dfs_nick_info:
                for site in tmp:
                    if (site.tag in ['localNickname', 'pseudoNickname', 'pseudoPriority']):
                        dfs_group_info[site.tag] = site.text
        return dfs_group_info