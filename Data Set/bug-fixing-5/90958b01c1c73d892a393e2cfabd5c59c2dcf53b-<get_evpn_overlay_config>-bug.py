def get_evpn_overlay_config(self):
    'get evpn-overlay enable configuration'
    flags = list()
    exp = '| ignore-case include evpn-overlay enable'
    flags.append(exp)
    return get_config(self.module, flags)