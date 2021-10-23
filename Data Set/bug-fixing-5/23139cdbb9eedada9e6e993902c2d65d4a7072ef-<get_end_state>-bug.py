def get_end_state(self):
    'Get end config'
    self.get_current_config()
    self.end_state = dict(as_number=self.as_number, bgp_instance=self.bgp_instance, peer_type=self.cur_config['peer_type'], peer=self.cur_config['peer'], bgp_evpn_enable=self.cur_config['bgp_evpn_enable'], reflect_client=self.cur_config['reflect_client'], policy_vpn_target=self.cur_config['policy_vpn_target'])