def get_evpn_global_info(self):
    ' get current EVPN global configuration'
    self.global_info['evpnOverLay'] = 'disable'
    flags = list()
    exp = ' | include evpn-overlay enable'
    flags.append(exp)
    config = get_config(self.module, flags)
    if config:
        self.global_info['evpnOverLay'] = 'enable'