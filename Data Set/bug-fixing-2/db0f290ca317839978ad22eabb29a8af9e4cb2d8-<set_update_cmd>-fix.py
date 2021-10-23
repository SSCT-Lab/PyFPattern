

def set_update_cmd(self):
    ' set update command'
    if (not self.changed):
        return
    if self.vpn_target_type:
        if (self.vpn_target_type == 'export_extcommunity'):
            vpn_target_type = 'export-extcommunity'
        else:
            vpn_target_type = 'import-extcommunity'
    if (self.state == 'present'):
        self.updates_cmd.append(('ip vpn-instance %s' % self.vrf))
        if (self.vrf_aftype == 'ipv4uni'):
            self.updates_cmd.append('ipv4-family')
        elif (self.vrf_aftype == 'ipv6uni'):
            self.updates_cmd.append('ipv6-family')
        if self.route_distinguisher:
            if (not self.is_vrf_rd_exist()):
                self.updates_cmd.append(('route-distinguisher %s' % self.route_distinguisher))
        elif (self.get_exist_rd() is not None):
            self.updates_cmd.append(('undo route-distinguisher %s' % self.get_exist_rd()))
        if (self.vpn_target_state == 'present'):
            if (not self.is_vrf_rt_exist()):
                if (self.evpn is False):
                    self.updates_cmd.append(('vpn-target %s %s' % (self.vpn_target_value, vpn_target_type)))
                else:
                    self.updates_cmd.append(('vpn-target %s %s evpn' % (self.vpn_target_value, vpn_target_type)))
        elif (self.vpn_target_state == 'absent'):
            if self.is_vrf_rt_exist():
                if (self.evpn is False):
                    self.updates_cmd.append(('undo vpn-target %s %s' % (self.vpn_target_value, vpn_target_type)))
                else:
                    self.updates_cmd.append(('undo vpn-target %s %s evpn' % (self.vpn_target_value, vpn_target_type)))
    else:
        self.updates_cmd.append(('ip vpn-instance %s' % self.vrf))
        if (self.vrf_aftype == 'ipv4uni'):
            self.updates_cmd.append('undo ipv4-family')
        elif (self.vrf_aftype == 'ipv6uni'):
            self.updates_cmd.append('undo ipv6-family')
