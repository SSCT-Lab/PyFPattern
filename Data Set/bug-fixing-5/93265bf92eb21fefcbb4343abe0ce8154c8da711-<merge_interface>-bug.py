def merge_interface(self, ifname, mtu):
    ' Merge interface mtu.'
    xmlstr = ''
    change = False
    self.updates_cmd.append(('interface %s' % ifname))
    if (self.state == 'present'):
        if (mtu and (self.intf_info['ifMtu'] != mtu)):
            xmlstr += (CE_NC_XML_MERGE_INTF_MTU % (ifname, mtu))
            self.updates_cmd.append(('mtu %s' % mtu))
            change = True
    elif (self.intf_info['ifMtu'] != '1500'):
        xmlstr += (CE_NC_XML_MERGE_INTF_MTU % (ifname, '1500'))
        self.updates_cmd.append('undo mtu')
        change = True
    if (not change):
        return
    conf_str = build_config_xml(xmlstr)
    ret_xml = set_nc_config(self.module, conf_str)
    self.check_response(ret_xml, 'MERGE_INTF_MTU')
    self.changed = True