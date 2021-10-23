def work(self):
    'worker'
    self.check_params()
    if (self.gratuitous_arp_interval or self.version or self.recover_delay):
        self.vrrp_global_info = self.get_vrrp_global_info()
    if (self.interface and self.vrid):
        self.virtual_ip_info = self.get_virtual_ip_info()
        if self.virtual_ip_info:
            self.vrrp_group_info = self.get_vrrp_group_info()
    self.get_proposed()
    self.get_existing()
    if (self.gratuitous_arp_interval or self.version or self.recover_delay):
        if (self.state == 'present'):
            self.set_vrrp_global()
        else:
            self.delete_vrrp_global()
    elif ((not self.interface) or (not self.vrid)):
        self.module.fail_json(msg='Error: interface, vrid must be config at the same time.')
    if (self.interface and self.vrid):
        if self.virtual_ip:
            if (self.state == 'present'):
                self.create_virtual_ip()
            else:
                self.delete_virtual_ip()
        else:
            if (not self.vrrp_group_info):
                self.module.fail_json(msg='Error: The VRRP group does not exist.')
            if (self.admin_ignore_if_down == 'true'):
                if (self.vrrp_type != 'admin'):
                    self.module.fail_json(msg='Error: vrrpType must be admin when admin_ignore_if_down is true.')
            if (self.admin_interface or self.admin_vrid):
                if (self.vrrp_type != 'member'):
                    self.module.fail_json(msg='Error: it binds a VRRP group to an mVRRP group, vrrp_type must be "member".')
                if ((not self.vrrp_type) or (not self.interface) or (not self.vrid)):
                    self.module.fail_json(msg='Error: admin_interface admin_vrid vrrp_type interface vrid must be config at the same time.')
            if ((self.auth_mode == 'md5') and (self.is_plain == 'true')):
                self.module.fail_json(msg='Error: is_plain can not be True when auth_mode is md5.')
            if (self.state == 'present'):
                self.set_vrrp_group()
            else:
                self.delete_vrrp_group()
    self.get_end_state()
    self.results['changed'] = self.changed
    self.results['proposed'] = self.proposed
    self.results['existing'] = self.existing
    self.results['end_state'] = self.end_state
    if self.changed:
        self.results['updates'] = self.updates_cmd
    else:
        self.results['updates'] = list()
    self.module.exit_json(**self.results)