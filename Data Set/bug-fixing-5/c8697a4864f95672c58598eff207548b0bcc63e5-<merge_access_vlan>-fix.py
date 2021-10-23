def merge_access_vlan(self, ifname, default_vlan):
    'Merge access interface vlan'
    change = False
    conf_str = ''
    self.updates_cmd.append(('interface %s' % ifname))
    if (self.state == 'present'):
        if (self.intf_info['linkType'] == 'access'):
            if (default_vlan and (self.intf_info['pvid'] != default_vlan)):
                self.updates_cmd.append(('port default vlan %s' % default_vlan))
                conf_str = (CE_NC_SET_PORT % (ifname, 'access', default_vlan, '', ''))
                change = True
        else:
            self.updates_cmd.append('port link-type access')
            if default_vlan:
                self.updates_cmd.append(('port default vlan %s' % default_vlan))
                conf_str = (CE_NC_SET_PORT % (ifname, 'access', default_vlan, '', ''))
            else:
                conf_str = (CE_NC_SET_PORT % (ifname, 'access', '1', '', ''))
            change = True
    elif (self.state == 'absent'):
        if (self.intf_info['linkType'] == 'access'):
            if (default_vlan and (self.intf_info['pvid'] == default_vlan) and (default_vlan != '1')):
                self.updates_cmd.append(('undo port default vlan %s' % default_vlan))
                conf_str = (CE_NC_SET_PORT % (ifname, 'access', '1', '', ''))
                change = True
    if (not change):
        self.updates_cmd.pop()
        return
    conf_str = (('<config>' + conf_str) + '</config>')
    rcv_xml = set_nc_config(self.module, conf_str)
    self.check_response(rcv_xml, 'MERGE_ACCESS_PORT')
    self.changed = True