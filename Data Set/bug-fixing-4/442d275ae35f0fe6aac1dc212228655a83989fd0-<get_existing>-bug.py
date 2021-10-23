def get_existing(self):
    'get existing info'
    if self.gratuitous_arp_interval:
        self.existing['gratuitous_arp_interval'] = self.vrrp_global_info['gratuitousArpTimeOut']
    if self.version:
        self.existing['version'] = self.vrrp_global_info['version']
    if self.recover_delay:
        self.existing['recover_delay'] = self.vrrp_global_info['recoverDelay']
    if self.virtual_ip:
        if self.virtual_ip_info:
            self.existing['interface'] = self.interface
            self.existing['vrid'] = self.vrid
            self.existing['virtual_ip_info'] = self.virtual_ip_info['vrrpVirtualIpInfos']
    if self.vrrp_group_info:
        self.existing['interface'] = self.vrrp_group_info['ifName']
        self.existing['vrid'] = self.vrrp_group_info['vrrpId']
        self.existing['vrrp_type'] = self.vrrp_group_info['vrrpType']
        if (self.vrrp_type == 'admin'):
            self.existing['admin_ignore_if_down'] = self.vrrp_group_info['authenticationMode']
        if (self.admin_vrid and self.admin_interface):
            self.existing['admin_vrid'] = self.vrrp_group_info['adminVrrpId']
            self.existing['admin_interface'] = self.vrrp_group_info['adminIfName']
            self.existing['admin_flowdown'] = self.vrrp_group_info['unflowdown']
        if self.priority:
            self.existing['priority'] = self.vrrp_group_info['priority']
        if self.advertise_interval:
            self.existing['advertise_interval'] = self.vrrp_group_info['advertiseInterval']
        if self.preempt_timer_delay:
            self.existing['preempt_timer_delay'] = self.vrrp_group_info['delayTime']
        if self.holding_multiplier:
            self.existing['holding_multiplier'] = self.vrrp_group_info['holdMultiplier']
        if self.fast_resume:
            fast_resume_exist = 'disable'
            fast_resume = self.vrrp_group_info['fastResume']
            if (fast_resume == 'true'):
                fast_resume_exist = 'enable'
            self.existing['fast_resume'] = fast_resume_exist
        if self.auth_mode:
            self.existing['auth_mode'] = self.vrrp_group_info['authenticationMode']
            self.existing['is_plain'] = self.vrrp_group_info['isPlain']