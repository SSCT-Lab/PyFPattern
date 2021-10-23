def check_params(self):
    'Check all input params'
    if self.interface:
        self.intf_type = get_interface_type(self.interface)
        if (not self.intf_type):
            self.module.fail_json(msg=('Error: Interface name of %s is error.' % self.interface))
    if (not self.intf_type):
        self.module.fail_json(msg='Error: Interface %s is error.')
    if self.mtu:
        if (not self.mtu.isdigit()):
            self.module.fail_json(msg='Error: Mtu is invalid.')
        if ((int(self.mtu) < 46) or (int(self.mtu) > 9600)):
            self.module.fail_json(msg='Error: Mtu is not in the range from 46 to 9600.')
    self.intf_info = self.get_interface_dict(self.interface)
    if (not self.intf_info):
        self.module.fail_json(msg='Error: interface does not exist.')
    if (self.mtu and (self.intf_info['isL2SwitchPort'] == 'true')):
        self.module.fail_json(msg='Error: L2Switch Port can not set mtu.')
    if (self.state == 'present'):
        if self.jbf_max:
            if (not is_interface_support_setjumboframe(self.interface)):
                self.module.fail_json(msg=('Error: Interface %s does not support jumboframe set.' % self.interface))
            if (not self.jbf_max.isdigit()):
                self.module.fail_json(msg='Error: Max jumboframe is not digit.')
            if ((int(self.jbf_max) > 12288) or (int(self.jbf_max) < 1536)):
                self.module.fail_json(msg='Error: Max jumboframe is between 1536 to 12288.')
        if self.jbf_min:
            if (not self.jbf_min.isdigit()):
                self.module.fail_json(msg='Error: Min jumboframe is not digit.')
            if (not self.jbf_max):
                self.module.fail_json(msg='Error: please specify max jumboframe value.')
            if ((int(self.jbf_min) > self.jbf_max) or (int(self.jbf_min) < 1518)):
                self.module.fail_json(msg='Error: Min jumboframe is between 1518 to jumboframe max value.')
        if (self.jbf_min is not None):
            if (self.jbf_max is None):
                self.module.fail_json(msg='Error: please input MAX jumboframe value.')