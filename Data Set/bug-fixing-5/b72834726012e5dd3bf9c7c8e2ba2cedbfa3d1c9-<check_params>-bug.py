def check_params(self):
    'Check all input params'
    if (not self.session_name):
        self.module.fail_json(msg='Error: Missing required arguments: session_name.')
    if self.session_name:
        if ((len(self.session_name) < 1) or (len(self.session_name) > 15)):
            self.module.fail_json(msg='Error: Session name is invalid.')
    if self.out_if_name:
        if (not get_interface_type(self.out_if_name)):
            self.module.fail_json(msg='Error: Session out_if_name is invalid.')
    if self.dest_addr:
        if (not check_ip_addr(self.dest_addr)):
            self.module.fail_json(msg='Error: Session dest_addr is invalid.')
    if self.src_addr:
        if (not check_ip_addr(self.src_addr)):
            self.module.fail_json(msg='Error: Session src_addr is invalid.')
    if self.vrf_name:
        if (not is_valid_ip_vpn(self.vrf_name)):
            self.module.fail_json(msg='Error: Session vrf_name is invalid.')
        if (not self.dest_addr):
            self.module.fail_json(msg='Error: vrf_name and dest_addr must set at the same time.')
    if (self.use_default_ip and (not self.out_if_name)):
        self.module.fail_json(msg='Error: use_default_ip and out_if_name must set at the same time.')