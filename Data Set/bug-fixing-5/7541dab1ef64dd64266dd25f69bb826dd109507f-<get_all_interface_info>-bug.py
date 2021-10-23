def get_all_interface_info(self, intf_type=None):
    'Get interface information all or by interface type'
    xml_str = (CE_NC_GET_INT_STATISTICS % '')
    con_obj = get_nc_config(self.module, xml_str)
    if ('<data/>' in con_obj):
        return
    xml_str = con_obj.replace('\r', '').replace('\n', '').replace('xmlns="urn:ietf:params:xml:ns:netconf:base:1.0"', '').replace('xmlns="http://www.huawei.com/netconf/vrp"', '')
    root = ElementTree.fromstring(xml_str)
    intfs_info = root.find('ifm/interfaces')
    if (not intfs_info):
        return
    intf_name = ''
    flag = False
    for eles in intfs_info:
        if (eles.tag == 'interface'):
            for ele in eles:
                if (ele.tag in ['ifName', 'ifDynamicInfo', 'ifStatistics', 'ifClearedStat']):
                    if (ele.tag == 'ifName'):
                        intf_name = ele.text.lower()
                        if intf_type:
                            if (get_interface_type(intf_name) != intf_type.lower()):
                                break
                            else:
                                flag = True
                        self.init_interface_data(intf_name)
                        if is_ethernet_port(intf_name):
                            self.get_port_info(intf_name)
                    if (ele.tag == 'ifDynamicInfo'):
                        self.get_intf_dynamic_info(ele, intf_name)
                    elif (ele.tag == 'ifStatistics'):
                        self.get_intf_statistics_info(ele, intf_name)
                    elif (ele.tag == 'ifClearedStat'):
                        self.get_intf_cleared_stat(ele, intf_name)
    if (intf_type and (not flag)):
        self.module.fail_json(msg=('Error: %s interface type does not exist.' % intf_type.upper()))