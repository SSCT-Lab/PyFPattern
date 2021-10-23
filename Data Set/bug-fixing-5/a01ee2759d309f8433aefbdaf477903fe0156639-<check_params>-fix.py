def check_params(self):
    'Check all input params'
    if self.interface:
        intf_type = get_interface_type(self.interface)
        if (not intf_type):
            self.module.fail_json(msg=('Error: Interface name of %s is error.' % self.interface))
    if self.vrid:
        if (not self.vrid.isdigit()):
            self.module.fail_json(msg='Error: The value of vrid is an integer.')
        if ((int(self.vrid) < 1) or (int(self.vrid) > 255)):
            self.module.fail_json(msg='Error: The value of vrid ranges from 1 to 255.')
    if self.virtual_ip:
        if (not is_valid_address(self.virtual_ip)):
            self.module.fail_json(msg=('Error: The %s is not a valid ip address.' % self.virtual_ip))
    if self.admin_vrid:
        if (not self.admin_vrid.isdigit()):
            self.module.fail_json(msg='Error: The value of admin_vrid is an integer.')
        if ((int(self.admin_vrid) < 1) or (int(self.admin_vrid) > 255)):
            self.module.fail_json(msg='Error: The value of admin_vrid ranges from 1 to 255.')
    if self.admin_interface:
        intf_type = get_interface_type(self.admin_interface)
        if (not intf_type):
            self.module.fail_json(msg=('Error: Admin interface name of %s is error.' % self.admin_interface))
    if self.priority:
        if (not self.priority.isdigit()):
            self.module.fail_json(msg='Error: The value of priority is an integer.')
        if ((int(self.priority) < 1) or (int(self.priority) > 254)):
            self.module.fail_json(msg='Error: The value of priority ranges from 1 to 254. The default value is 100.')
    if self.advertise_interval:
        if (not self.advertise_interval.isdigit()):
            self.module.fail_json(msg='Error: The value of advertise_interval is an integer.')
        if ((int(self.advertise_interval) < 1000) or (int(self.advertise_interval) > 255000)):
            self.module.fail_json(msg='Error: The value of advertise_interval ranges from 1000 to 255000 milliseconds. The default value is 1000 milliseconds.')
        if ((int(self.advertise_interval) % 1000) != 0):
            self.module.fail_json(msg='Error: The advertisement interval value of VRRP must be a multiple of 1000 milliseconds.')
    if self.preempt_timer_delay:
        if (not self.preempt_timer_delay.isdigit()):
            self.module.fail_json(msg='Error: The value of preempt_timer_delay is an integer.')
        if ((int(self.preempt_timer_delay) < 1) or (int(self.preempt_timer_delay) > 3600)):
            self.module.fail_json(msg='Error: The value of preempt_timer_delay ranges from 1 to 3600. The default value is 0.')
    if self.holding_multiplier:
        if (not self.holding_multiplier.isdigit()):
            self.module.fail_json(msg='Error: The value of holding_multiplier is an integer.')
        if ((int(self.holding_multiplier) < 3) or (int(self.holding_multiplier) > 10)):
            self.module.fail_json(msg='Error: The value of holding_multiplier ranges from 3 to 10. The default value is 3.')
    if self.auth_key:
        if ((len(self.auth_key) > 16) or (len(self.auth_key.replace(' ', '')) < 1)):
            self.module.fail_json(msg='Error: The length of auth_key is not in the range from 1 to 16.')