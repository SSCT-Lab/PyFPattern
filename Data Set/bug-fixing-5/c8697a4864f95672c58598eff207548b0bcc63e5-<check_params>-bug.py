def check_params(self):
    'Check all input params'
    if self.interface:
        self.intf_type = get_interface_type(self.interface)
        if (not self.intf_type):
            self.module.fail_json(msg=('Error: Interface name of %s is error.' % self.interface))
    if ((not self.intf_type) or (not is_portswitch_enalbed(self.intf_type))):
        self.module.fail_json(msg='Error: Interface %s is error.')
    if self.access_vlan:
        if (not self.access_vlan.isdigit()):
            self.module.fail_json(msg='Error: Access vlan id is invalid.')
        if ((int(self.access_vlan) <= 0) or (int(self.access_vlan) > 4094)):
            self.module.fail_json(msg='Error: Access vlan id is not in the range from 1 to 4094.')
    if self.native_vlan:
        if (not self.native_vlan.isdigit()):
            self.module.fail_json(msg='Error: Native vlan id is invalid.')
        if ((int(self.native_vlan) <= 0) or (int(self.native_vlan) > 4094)):
            self.module.fail_json(msg='Error: Native vlan id is not in the range from 1 to 4094.')
    self.intf_info = self.get_interface_dict(self.interface)
    if (not self.intf_info):
        self.module.fail_json(msg='Error: Interface does not exist.')
    if (not self.is_l2switchport()):
        self.module.fail_json(msg='Error: Interface is not layer2 swtich port.')