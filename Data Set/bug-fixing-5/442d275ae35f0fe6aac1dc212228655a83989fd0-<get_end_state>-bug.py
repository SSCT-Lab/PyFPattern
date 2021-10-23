def get_end_state(self):
    'get end state info'
    if (self.gratuitous_arp_interval or self.version or self.recover_delay):
        self.vrrp_global_info = self.get_vrrp_global_info()
    if (self.interface and self.vrid):
        if self.virtual_ip:
            self.virtual_ip_info = self.get_virtual_ip_info()
        if self.virtual_ip_info:
            self.vrrp_group_info = self.get_vrrp_group_info()
    if self.gratuitous_arp_interval:
        self.end_state['gratuitous_arp_interval'] = self.vrrp_global_info['gratuitousArpTimeOut']
    if self.version:
        self.end_state['version'] = self.vrrp_global_info['version']
    if self.recover_delay:
        self.end_state['recover_delay'] = self.vrrp_global_info['recoverDelay']
    if self.virtual_ip:
        if self.virtual_ip_info:
            self.end_state['interface'] = self.interface
            self.end_state['vrid'] = self.vrid
            self.end_state['virtual_ip_info'] = self.virtual_ip_info['vrrpVirtualIpInfos']
    if self.vrrp_group_info:
        self.end_state['interface'] = self.vrrp_group_info['ifName']
        self.end_state['vrid'] = self.vrrp_group_info['vrrpId']
        self.end_state['vrrp_type'] = self.vrrp_group_info['vrrpType']
        if (self.vrrp_type == 'admin'):
            self.end_state['admin_ignore_if_down'] = self.vrrp_group_info['authenticationMode']
        if (self.admin_vrid and self.admin_interface):
            self.existing['admin_vrid'] = self.vrrp_group_info['adminVrrpId']
            self.end_state['admin_interface'] = self.vrrp_group_info['adminIfName']
            self.end_state['admin_flowdown'] = self.vrrp_group_info['unflowdown']
        if self.priority:
            self.end_state['priority'] = self.vrrp_group_info['priority']
        if self.advertise_interval:
            self.end_state['advertise_interval'] = self.vrrp_group_info['advertiseInterval']
        if self.preempt_timer_delay:
            self.end_state['preempt_timer_delay'] = self.vrrp_group_info['delayTime']
        if self.holding_multiplier:
            self.end_state['holding_multiplier'] = self.vrrp_group_info['holdMultiplier']
        if self.fast_resume:
            fast_resume_end = 'disable'
            fast_resume = self.vrrp_group_info['fastResume']
            if (fast_resume == 'true'):
                fast_resume_end = 'enable'
            self.end_state['fast_resume'] = fast_resume_end
        if self.auth_mode:
            self.end_state['auth_mode'] = self.vrrp_group_info['authenticationMode']
            self.end_state['is_plain'] = self.vrrp_group_info['isPlain']