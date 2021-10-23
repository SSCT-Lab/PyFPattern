def merge_trunk_vlan(self, ifname, native_vlan, trunk_vlans):
    'Merge trunk interface vlan'
    change = False
    xmlstr = ''
    self.updates_cmd.append(('interface %s' % ifname))
    if trunk_vlans:
        vlan_list = self.vlan_range_to_list(trunk_vlans)
        vlan_map = self.vlan_list_to_bitmap(vlan_list)
    if (self.state == 'present'):
        if (self.intf_info['linkType'] == 'trunk'):
            if (native_vlan and (self.intf_info['pvid'] != native_vlan)):
                self.updates_cmd.append(('port trunk pvid vlan %s' % native_vlan))
                xmlstr += (CE_NC_SET_TRUNK_PORT_PVID % (ifname, native_vlan))
                change = True
            if trunk_vlans:
                add_vlans = self.vlan_bitmap_add(self.intf_info['trunkVlans'], vlan_map)
                if (not is_vlan_bitmap_empty(add_vlans)):
                    self.updates_cmd.append(('port trunk allow-pass %s' % trunk_vlans.replace(',', ' ').replace('-', ' to ')))
                    xmlstr += (CE_NC_SET_TRUNK_PORT_VLANS % (ifname, add_vlans, add_vlans))
                    change = True
        else:
            self.updates_cmd.append('port link-type trunk')
            change = True
            if native_vlan:
                self.updates_cmd.append(('port trunk pvid vlan %s' % native_vlan))
                xmlstr += (CE_NC_SET_TRUNK_PORT_PVID % (ifname, native_vlan))
            if trunk_vlans:
                self.updates_cmd.append(('port trunk allow-pass %s' % trunk_vlans.replace(',', ' ').replace('-', ' to ')))
                xmlstr += (CE_NC_SET_TRUNK_PORT_VLANS % (ifname, vlan_map, vlan_map))
            if ((not native_vlan) and (not trunk_vlans)):
                xmlstr += (CE_NC_SET_TRUNK_PORT_MODE % ifname)
                self.updates_cmd.append('undo port trunk allow-pass vlan 1')
    elif (self.state == 'absent'):
        if (self.intf_info['linkType'] == 'trunk'):
            if (native_vlan and (self.intf_info['pvid'] == native_vlan) and (native_vlan != '1')):
                self.updates_cmd.append(('undo port trunk pvid vlan %s' % native_vlan))
                xmlstr += (CE_NC_SET_TRUNK_PORT_PVID % (ifname, 1))
                change = True
            if trunk_vlans:
                del_vlans = self.vlan_bitmap_del(self.intf_info['trunkVlans'], vlan_map)
                if (not is_vlan_bitmap_empty(del_vlans)):
                    self.updates_cmd.append(('undo port trunk allow-pass %s' % trunk_vlans.replace(',', ' ').replace('-', ' to ')))
                    undo_map = vlan_bitmap_undo(del_vlans)
                    xmlstr += (CE_NC_SET_TRUNK_PORT_VLANS % (ifname, undo_map, del_vlans))
                    change = True
        else:
            self.updates_cmd.append('port link-type trunk')
            self.updates_cmd.append('undo port trunk allow-pass vlan 1')
            xmlstr += (CE_NC_SET_TRUNK_PORT_MODE % ifname)
            change = True
    if (not change):
        self.updates_cmd.pop()
        return
    conf_str = (('<config>' + xmlstr) + '</config>')
    rcv_xml = set_nc_config(self.module, conf_str)
    self.check_response(rcv_xml, 'MERGE_TRUNK_PORT')
    self.changed = True