

def get_ospf_dict(self):
    ' get one ospf attributes dict.'
    ospf_info = dict()
    conf_str = (CE_NC_GET_OSPF % (self.process_id, self.get_area_ip(), self.interface))
    rcv_xml = get_nc_config(self.module, conf_str)
    if ('<data/>' in rcv_xml):
        return ospf_info
    xml_str = rcv_xml.replace('\r', '').replace('\n', '').replace('xmlns="urn:ietf:params:xml:ns:netconf:base:1.0"', '').replace('xmlns="http://www.huawei.com/netconf/vrp"', '')
    root = ElementTree.fromstring(xml_str)
    ospfsite = root.find('ospfv2/ospfv2comm/ospfSites/ospfSite')
    if (not ospfsite):
        self.module.fail_json(msg='Error: ospf process does not exist.')
    for site in ospfsite:
        if (site.tag in ['processId', 'routerId', 'vrfName']):
            ospf_info[site.tag] = site.text
    ospf_info['areaId'] = ''
    areas = root.find('ospfv2/ospfv2comm/ospfSites/ospfSite/areas/area')
    if areas:
        for area in areas:
            if (area.tag == 'areaId'):
                ospf_info['areaId'] = area.text
                break
    ospf_info['interface'] = dict()
    intf = root.find('ospfv2/ospfv2comm/ospfSites/ospfSite/areas/area/interfaces/interface')
    if intf:
        for attr in intf:
            if (attr.tag in ['ifName', 'networkType', 'helloInterval', 'deadInterval', 'silentEnable', 'configCost', 'authenticationMode', 'authTextSimple', 'keyId', 'authTextMd5']):
                ospf_info['interface'][attr.tag] = attr.text
    return ospf_info
