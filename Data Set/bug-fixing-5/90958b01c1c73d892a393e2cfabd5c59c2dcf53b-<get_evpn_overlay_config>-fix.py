def get_evpn_overlay_config(self):
    'get evpn-overlay enable configuration'
    cmd = 'display current-configuration | include ^evpn-overlay enable'
    (rc, out, err) = exec_command(self.module, cmd)
    if (rc != 0):
        self.module.fail_json(msg=err)
    return out