def check_params(self):
    'Check all input params'
    if self.interface:
        self.intf_type = get_interface_type(self.interface)
        if (not self.intf_type):
            self.module.fail_json(msg=('Error: Interface name of %s is error.' % self.interface))
    if ((not self.intf_type) or (not is_portswitch_enalbed(self.intf_type))):
        self.module.fail_json(msg='Error: Interface %s is error.')
    if self.default_vlan:
        if (not self.default_vlan.isdigit()):
            self.module.fail_json(msg='Error: Access vlan id is invalid.')
        if ((int(self.default_vlan) <= 0) or (int(self.default_vlan) > 4094)):
            self.module.fail_json(msg='Error: Access vlan id is not in the range from 1 to 4094.')
    if self.pvid_vlan:
        if (not self.pvid_vlan.isdigit()):
            self.module.fail_json(msg='Error: Pvid vlan id is invalid.')
        if ((int(self.pvid_vlan) <= 0) or (int(self.pvid_vlan) > 4094)):
            self.module.fail_json(msg='Error: Pvid vlan id is not in the range from 1 to 4094.')
    self.intf_info = self.get_interface_dict(self.interface)
    if (not self.intf_info):
        self.module.fail_json(msg='Error: Interface does not exist.')
    if (not self.is_l2switchport()):
        self.module.fail_json(msg='Error: Interface is not layer2 swtich port.')
    if (self.state == 'unconfigured'):
        if any([self.mode, self.default_vlan, self.pvid_vlan, self.trunk_vlans, self.untagged_vlans, self.tagged_vlans]):
            self.module.fail_json(msg='Error: When state is unconfigured, only interface name exists.')
    elif (self.mode == 'access'):
        if any([self.pvid_vlan, self.trunk_vlans, self.untagged_vlans, self.tagged_vlans]):
            self.module.fail_json(msg='Error: When mode is access, only default_vlan can be supported.')
    elif (self.mode == 'trunk'):
        if any([self.default_vlan, self.untagged_vlans, self.tagged_vlans]):
            self.module.fail_json(msg='Error: When mode is trunk, only pvid_vlan and trunk_vlans can exist.')
    elif (self.mode == 'hybrid'):
        if any([self.default_vlan, self.trunk_vlans]):
            self.module.fail_json(msg='Error: When mode is hybrid, default_vlan and trunk_vlans cannot exist')
    elif any([self.pvid_vlan, self.trunk_vlans, self.untagged_vlans, self.tagged_vlans]):
        self.module.fail_json(msg='Error: When mode is dot1qtunnel, only default_vlan can be supported.')