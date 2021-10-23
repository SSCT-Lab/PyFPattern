def enough_space(self):
    'Whether device has enough space'
    xml_str = CE_NC_GET_DISK_INFO
    ret_xml = get_nc_config(self.module, xml_str)
    if ('<data/>' in ret_xml):
        return
    xml_str = ret_xml.replace('\r', '').replace('\n', '').replace('xmlns="urn:ietf:params:xml:ns:netconf:base:1.0"', '').replace('xmlns="http://www.huawei.com/netconf/vrp"', '')
    root = ElementTree.fromstring(xml_str)
    topo = root.find('vfm/dfs/df/freeSize')
    kbytes_free = topo.text
    file_size = os.path.getsize(self.local_file)
    if ((int(kbytes_free) * 1024) > file_size):
        return True
    return False