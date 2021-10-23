def get_end_state(self):
    'get end state info'
    self.config = self.get_current_config()
    if (not self.config):
        return
    self.config_list = self.config.split('l2vpn-family evpn')
    if (len(self.config_list) == 2):
        self.l2vpn_evpn_exist = True
    if self.bgp_instance:
        self.end_state['bgp_instance'] = self.bgp_instance
    if (self.peer_address and self.peer_enable):
        if self.l2vpn_evpn_exist:
            self.end_state['peer_address_enable'] = self.get_peers_enable()
    if (self.peer_group_name and self.peer_enable):
        if self.l2vpn_evpn_exist:
            self.end_state['peer_group_enable'] = self.get_peers_group_enable()
    if (self.peer_address and self.advertise_router_type):
        if self.l2vpn_evpn_exist:
            self.end_state['peer_address_advertise_type'] = self.get_peers_advertise_type()
    if (self.peer_group_name and self.advertise_router_type):
        if self.l2vpn_evpn_exist:
            self.end_state['peer_group_advertise_type'] = self.get_peer_groups_advertise_type()
    if (self.advertise_l2vpn_evpn and self.vpn_name):
        cmd = (' ipv4-family vpn-instance %s' % self.vpn_name)
        exist = is_config_exist(self.config, cmd)
        if exist:
            self.end_state['vpn_name'] = self.vpn_name
            l2vpn_cmd = 'advertise l2vpn evpn'
            l2vpn_exist = is_config_exist(self.config, l2vpn_cmd)
            if l2vpn_exist:
                self.end_state['advertise_l2vpn_evpn'] = 'enable'
            else:
                self.end_state['advertise_l2vpn_evpn'] = 'disable'