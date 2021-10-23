def get_evpn_global_info(self):
    ' get current EVPN global configuration'
    self.global_info['evpnOverLay'] = 'disable'
    cmd = 'display current-configuration | include ^evpn-overlay enable'
    (rc, out, err) = exec_command(self.module, cmd)
    if (rc != 0):
        self.module.fail_json(msg=err)
    if out:
        self.global_info['evpnOverLay'] = 'enable'