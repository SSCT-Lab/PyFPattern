def is_vrrp_group_info_change(self):
    'whether vrrp group attribute info change'
    if self.vrrp_type:
        if (self.vrrp_group_info['vrrpType'] != self.vrrp_type):
            return True
    if self.admin_ignore_if_down:
        if (self.vrrp_group_info['adminIgnoreIfDown'] != self.admin_ignore_if_down):
            return True
    if self.admin_vrid:
        if (self.vrrp_group_info['adminVrrpId'] != self.admin_vrid):
            return True
    if self.admin_interface:
        if (self.vrrp_group_info['adminIfName'] != self.admin_interface):
            return True
    if self.admin_flowdown:
        if (self.vrrp_group_info['unflowdown'] != self.admin_flowdown):
            return True
    if self.priority:
        if (self.vrrp_group_info['priority'] != self.priority):
            return True
    if self.fast_resume:
        fast_resume = 'false'
        if (self.fast_resume == 'enable'):
            fast_resume = 'true'
        if (self.vrrp_group_info['fastResume'] != fast_resume):
            return True
    if self.advertise_interval:
        if (self.vrrp_group_info['advertiseInterval'] != self.advertise_interval):
            return True
    if self.preempt_timer_delay:
        if (self.vrrp_group_info['delayTime'] != self.preempt_timer_delay):
            return True
    if self.holding_multiplier:
        if (self.vrrp_group_info['holdMultiplier'] != self.holding_multiplier):
            return True
    if self.auth_mode:
        if (self.vrrp_group_info['authenticationMode'] != self.auth_mode):
            return True
    if self.auth_key:
        return True
    if self.is_plain:
        if (self.vrrp_group_info['isPlain'] != self.is_plain):
            return True
    return False